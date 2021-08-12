# -*- coding: utf-8 -*-
from .regexanalyzer import RegexAnalyzer


class IPv4AddressAnalyzer(RegexAnalyzer):
    """Analyzer to match on ip addresses via regex"""
    name = "IPv4AddressAnalyzer"

    def __init__(self, actions):
        regex = r"\b\d{1,3}(?:\.\d{1,3}){3}\b"
        super().__init__(actions, regex)

    def verify(self, results):
        """Verify results to get only real IP adresses"""
        verified_ips = []
        for result in results:
            # Check each IP
            octet_max_value = 255
            for octet in result.split("."):
                if int(octet) > octet_max_value:
                    break
            else:
                # IP is valid
                verified_ips.append(result)

        return verified_ips
