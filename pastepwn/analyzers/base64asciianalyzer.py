# -*- coding: utf-8 -*-
from .base64analyzer import Base64Analyzer
from base64 import b64decode
import binascii


class Base64AsciiAnalyzer(Base64Analyzer):
    """Analyzer to match base64 strings which decode to valid ASCII"""
    name = "Base64AsciiAnalyzer"

    def __init__(self, actions, min_len=1, decode=False):
        super().__init__(actions, min_len)
        self.decode = decode

    def verify(self, results):
        """Method to determine if found base64 decodes to valid ASCII"""
        # find valid base64 strings with the parent class
        validated_strings = super().verify(results)

        # go through each base64 string and attempt to decode
        base64_ascii_strings = []

        for validated_string in validated_strings:
            # Check if the string is valid base64
            try:
                decoded_string = b64decode(validated_string)
            except binascii.Error:
                # The string is no valid base64
                continue

            # Check if the valid base64 decodes to plain ascii
            try:
                b64_ascii_string = decoded_string.decode("ascii")
            except UnicodeDecodeError:
                continue

            if self.decode:
                base64_ascii_strings.append(b64_ascii_string)
            else:
                base64_ascii_strings.append(validated_string)

        return base64_ascii_strings
