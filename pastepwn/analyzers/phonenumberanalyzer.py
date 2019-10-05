from .regexanalyzer import RegexAnalyzer

class PhoneNumberAnalyzer(RegexAnalyzer):
    """Analyzer to match Phone Numbers"""

    def __init__(self, action):
        """Analyzer to match international phone numbers"""
        # from stackoverflow: https://stackoverflow.com/questions/2113908/what-regular-expression-will-match-valid-international-phone-numbers
        country_code_regex = "\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)"

        # adapted from the same stackoverflow
        national_number = "(\W*\d){2,17}"

        regex = "(^|\s)" + country_code_regex + "\s*" + national_number + "($|\s)"

        super().__init__(action, regex)
