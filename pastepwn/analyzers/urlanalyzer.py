# -*- coding: utf-8 -*-
import re
import urllib.error
import urllib.request

from .basicanalyzer import BasicAnalyzer


class URLAnalyzer(BasicAnalyzer):
    """
    This analyzer detects url-like patterns using regex,
    and then optionally attempts to verify that they can
    be resolved.
    """
    name = "URLAnalyzer"

    def __init__(self, actions, regex, resolve=False):
        super().__init__(actions, regex)
        self.regex = re.compile(regex)
        self.resolve = resolve  # Should we try to resolve the URLs?

    def _resolve_url(self, url):
        """
        A helper method that tries to resolve a given URL.
        Returns False if the URL cannot be resolved.
        """

        # If the url doesn't start with a protocol, we'll test with http and https.
        if not url.startswith("http"):
            for protocol in ("http", "https"):
                # If adding the protocol makes this resolve, the url works.
                if self._resolve_url("{0}://{1}".format(protocol, url)):
                    return True
            else:
                return False

        # Otherwise, let's just try resolving it.
        else:
            try:
                urllib.request.urlopen(url)
            except urllib.error.URLError:
                return False
            return True

    def match(self, paste):
        """ Check if the URL matches a certain regex, and then optionally try to resolve it. """
        paste_content = paste.body
        match = self.regex.search(paste_content)
        is_regex = match is not None

        if match:
            url = match.group(0)

        # Optionally check if the url resolves.
        if is_regex and self.resolve:
            return self._resolve_url(url)

        return is_regex
