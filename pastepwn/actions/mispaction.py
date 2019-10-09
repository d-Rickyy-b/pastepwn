# -*- coding: utf-8 -*-
import json
import logging
from pastepwn.util import Request
from .basicaction import BasicAction


class MISPAction(BasicAction):
    """Action to add an event to a MISP instance on a matched paste"""
    name = "MISPAction"

    def __init__(self, url: str, access_key: str, transformer=None):
        """
        Init method for the MISPAction
        :param url:         string      URL of the MISP instance (complete with protocol and port)
        :param access_key:  string      MISP access key for authorization
        :param transformer: Callable    Takes a Paste (and optional analyzer name) as parameter 
                                        and returns a MISP-formatted event as a dictionary
        """
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.url = url
        self.access_key = access_key
        if transformer is None:
            self.transformer = MISPAction.default_transformer
        else:
            self.transformer = transformer

    @staticmethod
    def default_transformer(paste, analyzer_name=None) -> dict:
        # WIP - Sample data from MISP docs
        return {"date":"2015-01-01","threat_level_id":"1","info":"testevent","published":False,"analysis":"0","distribution":"0","Attribute":[{"type":"domain","category":"Network activity","to_ids":False,"distribution":"0","comment":"","value":"test.com"}]}

    def perform(self, paste, analyzer_name=None):
        """
        Sends the event to the MISP instance.
        :param paste: The paste passed by the ActionHandler
        :param analyzer_name: The name of the analyzer which matched the paste
        """
        # Call transformer to construct payload
        event = self.transformer(paste)
        data = json.dumps({"Event": event})
        # Send event to MISP instance
        r = Request()
        r.headers = {'Authorization': self.access_key, 'Accept': 'application/json', 'Content-Type': 'application/json'}
        res = r.post(self.url + "/events", data=data)
        # Error handling
        if not res:
            self.logger.warning("Empty response when adding event")
        else:
            res = json.loads(res)
            if 'Event' in res:
                self.logger.info('Event #%s successfully added to MIPS', res['Event']['id'])
            else:
                # An error has happend, but the 'errors' field is not always present
                if 'errors' in res:
                    self.logger.error('Error when adding event: %s', res['errors'])
                self.logger.warning('Failed to add event: %s', res.get('message'))
