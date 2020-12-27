# -*- coding: utf-8 -*-
import json
import logging
import time

from pastepwn.util import Request
from .basicaction import BasicAction


class MISPAction(BasicAction):
    """
    Action to add an event to a MISP instance on a matched paste

    Documentation for adding events:
    https://www.circl.lu/doc/misp/automation/#post-events

    The MISPAction objects can take a `transformer` function as a constructor parameter.
    This function (by default MISPAction.default_transformer) should take a Paste and an
    optional analyzer name as parameters (just like BasicAction.perform), and return a
    dictionary representing a MISP event, which will then be sent to the API.

    Additional attributes can be sent with each event, specified by the `attributes`
    parameter. Here is the documentation regarding types and categories:
    https://www.circl.lu/doc/misp/categories-and-types/
    """
    name = "MISPAction"

    def __init__(self, url, access_key, transformer=None, attributes=None):
        """Init method for the MISPAction
        :param url:         string      URL of the MISP instance (complete with protocol and port)
        :param access_key:  string      MISP access key for authorization
        :param transformer: Callable    Takes a Paste (and optional analyzer name) as parameter
                                        and returns a MISP-formatted event as a dictionary
        :param attributes:  Iterable    List of fully defined attributes to add to events
        """
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.url = url
        self.access_key = access_key
        if transformer is None:
            self.transformer = MISPAction.default_transformer
        else:
            self.transformer = transformer
        self.attributes = attributes

    @staticmethod
    def default_transformer(paste, analyzer_name=None):
        timestamp = time.gmtime(int(paste.date))
        attrs = []
        # Build event
        event = {
            "date": time.strftime("%Y-%m-%d", timestamp),
            "info": "Sensitive information found on pastebin (type: %s)" % analyzer_name,
            "threat_level_id": 4,   # Undefined
            "published": False,     # Unpublished
            "analysis": 0,          # Not yet analyzed
            "distribution": 0,      # Shared with organization only
            "Attribute": []
            }
        # Add link to the paste
        attrs.append({
            "type": "url",
            "category": "Network activity",
            "comment": "Link to pastebin paste containing information",
            "value": paste.full_url
            })
        # Add username of the author
        attrs.append({
            "type": "text",
            "category": "Attribution",
            "comment": "Username of paste author",
            "value": paste.user
            })
        # Add size of the paste
        attrs.append({
            "type": "size-in-bytes",
            "category": "Other",
            "comment": "Size of the paste",
            "value": paste.size
            })
        # Attach full paste if it's small
        if int(paste.size) <= 1024 and paste.body is not None:
            attrs.append({
                "type": "attachment",
                "category": "Artifacts dropped",
                "comment": "Raw body of the paste",
                "value": paste.body
                })
        # Add attributes to the event
        event["Attribute"] = attrs
        return event

    def perform(self, paste, analyzer_name=None, matches=None):
        """
        Sends the event to the MISP instance.
        :param paste: The paste passed by the ActionHandler
        :param analyzer_name: The name of the analyzer which matched the paste
        """
        # Call transformer to construct payload
        event = self.transformer(paste, analyzer_name)
        if self.attributes:
            # Add extra attributes
            event["Attributes"].extend(self.attributes)
        data = json.dumps({"Event": event})
        # Send event to MISP instance
        r = Request()
        r.headers = {"Authorization": self.access_key, "Accept": "application/json", "Content-Type": "application/json"}
        events_url = "{0}/events".format(self.url)
        res = r.post(events_url, data=data)

        # Error handling
        if not res:
            self.logger.warning("Empty response when adding event")
            return

        res = json.loads(res)
        if "Event" in res:
            event = res.get("Event")
            self.logger.info("Event #%s successfully added to MISP", event.get("id"))
            return
        # An error has happened, but the 'errors' field is not always present
        if "errors" in res:
            self.logger.error("Error when adding event: %s", res.get("errors"))
        self.logger.warning("Failed to add event: %s", res.get("message"))
