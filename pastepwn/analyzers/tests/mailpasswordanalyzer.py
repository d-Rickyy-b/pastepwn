# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers import MailPasswordAnalyzer


class TestMailPasswordAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = MailPasswordAnalyzer(None)
        self.paste = mock.Mock()

    def test_match_positive(self):
        """Test if positives are recognized"""

        positives = [
            "thesaxmaniac@hotmail.com:neverhood",
            "ledzepln1@aol.com:stairway",
            "kelsean75@hotmail.com:computer1elray8379@gmail.com:josh8598",
            "mekim45@hotmail.com:mullins74",
            "jjenkins19@yahoo.com:faster",
            "r_m_vincent@yahoo.com:soling12",
            "deadally@hotmail.com:balajaga1",
            "Choas23@gmail.com:8KlAs432",
            "jefftrey@yahoo.com:tanqueray",
            "syntex05@mac.com:kobela87",
            "michaelbarbra@hotmail.com:2177",
            "mcginnis_98@yahoo.com:bentley",
            "majikcityqban82@gmail.com:tinpen39",
            "pekanays@yahoo.com:warriors",
            "g_vanmeter@yahoo.com:torbeet",
            "rrothn@yahoo.com:rebsopjul3",
            "apryle_douglas@yahoo.com:campbell",
            "estocanam2@gmail.com:Firebird1@",
            "Samirenzer@yahoo.com:pepper0120",
            "davebialik@gmail.com:tr1ang1e",
            "kellyjames@atmc.net:ginnyanna",
            "Kennedy123@aol.com:Edmonia1",
            "rcstanley@ms.metrocast.net:jjba1304",
            "this_isatest@example.org:hello,world"
            "this-is-another-thest@müller-beispiel.de",
        ]

        for positive in positives:
            self.paste.body = positive
            self.assertTrue(
                self.analyzer.match(self.paste), f"{positive} do not match."
            )

    def test_match_negative(self):
        """Test if negatives are not recognized"""

        negatives = [
            "",
            None,
            "test@example.org",
            "example@:hello",
            "example@example:hello",
            "hello:test@example.org",
        ]

        for negative in negatives:
            self.paste.body = negative
            self.assertFalse(self.analyzer.match(self.paste), f"{negative} matches.")


if __name__ == "__main__":
    unittest.main()
