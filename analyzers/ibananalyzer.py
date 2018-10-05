# -*- coding: utf-8 -*-
import re

from .regexanalyzer import RegexAnalyzer


class IBANAnalyzer(RegexAnalyzer):
    def __init__(self, action, validate=False):
        # Regex taken from https://stackoverflow.com/a/44657292/3621482
        regex = "([A-Z]{2}[ \-]?[0-9]{2})" \
                "(?=(?:[ \-]?[A-Z0-9]){9,30}$)" \
                "((?:[ \-]?[A-Z0-9]{3,5}){2,7})" \
                "([ \-]?[A-Z0-9]{1,3})?$"
        super().__init__(action, regex)
        self.validate = validate

    def match(self, paste):
        paste_content = paste.body
        search_result = self.regex.search(paste_content)

        if search_result is None:
            return False

        if self.validate:
            matched_string = ''.join(search_result.groups())
            return self._validate_iban(matched_string)

        return True

    def _validate_iban(self, potential_iban):
        """From https://rosettacode.org/wiki/IBAN#Python"""

        # Ensure upper alphanumeric input.
        potential_iban = potential_iban.replace(' ', '').replace('\t', '').replace('-', '')
        if not re.match(r'^[\dA-Z]+$', potential_iban):
            return False

        # Validate country code against expected length.
        country_code = potential_iban[:2]
        if country_code not in self._country2length.keys() or len(potential_iban) != self._country2length[country_code]:
            return False

        # Shift and convert.
        potential_iban = potential_iban[4:] + potential_iban[:4]
        digits = int(''.join(str(int(ch, 36)) for ch in potential_iban))  # BASE 36: 0..9,A..Z -> 0..35
        return digits % 97 == 1

    _country2length = dict(
        AL=28, AD=24, AT=20, AZ=28, BE=16, BH=22, BA=20, BR=29,
        BG=22, CR=21, HR=21, CY=28, CZ=24, DK=18, DO=28, EE=20,
        FO=18, FI=18, FR=27, GE=22, DE=22, GI=23, GR=27, GL=18,
        GT=28, HU=28, IS=26, IE=22, IL=23, IT=27, KZ=20, KW=30,
        LV=21, LB=28, LI=21, LT=20, LU=20, MK=19, MT=31, MR=27,
        MU=30, MC=27, MD=24, ME=22, NL=18, NO=15, PK=24, PS=29,
        PL=28, PT=25, RO=24, SM=27, SA=24, RS=22, SK=24, SI=19,
        ES=24, SE=24, CH=21, TN=24, TR=26, AE=23, GB=22, VG=24)