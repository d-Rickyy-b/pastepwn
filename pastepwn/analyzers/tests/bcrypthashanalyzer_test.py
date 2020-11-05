# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.actions.basicaction import BasicAction
from pastepwn.analyzers.bcrypthashanalyzer import BcryptHashAnalyzer


class TestBcryptHashAnalyzer(unittest.TestCase):
    def setUp(self):
        """
        Sets the thread.

        Args:
            self: (todo): write your description
        """
        self.analyzer = BcryptHashAnalyzer(None)
        self.paste = mock.Mock()

    def test_match(self):
        """
        Validate the match.

        Args:
            self: (todo): write your description
        """
        valid_hashes = ["$2a$10$BIgnlSmYE8qYiONM0NQ53eRWBw5G4HIJEbXKzcsRVt.08IDnqH/V.",
                        "$2a$11$EppiRqR0kG9EKy56edDWTOnsv/oGW0dqAJB9ucmn3augbmcm8v/iy",
                        "$2b$10$FpOpno43SIE8e1hWnlOdR.9hG2J8dd5FD1kQq8hn4zLdKa5eIiFUO",
                        "$2a$10$SVy7GlMnWsemiZByHSnV0O3WoEHGImFt8v07uH.K3ZXwH5j9o/DP.",
                        "$2a$10$59SNkcZ0rdC2VgeWaavVyea9PFget/xmtbV7.9IeJl3CUq.Q954i2",
                        "$2b$10$Y8CJ9YIwrxt1YYgMqqU1delCYoTpIl18SRtYYI2kyM3jduKPHvWMC",
                        "$2a$10$2tNCUb.FUpSutyhkbqmMBuNnLzhqI4q9Miqurnj6eu.XsiIjww7I6",
                        "$2a$10$OyrADUFmj9QEqsd8frkEDOEYSPQalW5qoI1s2z6taCWwgUsjKzk5m"]

        invalid_hashes = ["7168D46050573DDA4CE409FA1515638BD28E86346D45F686310ED0678172BABCD4117FD15DD380B964352FE879FB745B573A730D526BB1188B2790FBA06E8ACA",
                          "5FD924625F6AB16A19CC9807C7C506AE1813490E4BA675F843D5A10E0BAACDB8",
                          "522F02FEA11E70C03C90C247C50410443246BFCB",
                          "8433FD5A3B0ED71D21CFB9F291BD89B9",
                          "$2a$124$SVy7GlMnWsemiZByHSnV0O3WoEHGImFt8v07uH.K3ZXwH5j9o/DP.a",
                          "$2a$12$SVy7GlMnWsemiZByHSnV0O3WoEHGImFt8v{07uH.K3ZXwH5j9o/DP.a",
                          "$2a$14$SVy7GlMnWsemiZByHSnV0O3WGImFt8v07uH.K3ZXwH5j9o/DP.a",
                          "@x,Y8q+jnYeZr$;",
                          "This is a test",
                          "$2a$10$   asdf 1234 how are you?"]

        for test_hash in valid_hashes:
            self.paste.body = test_hash
            self.assertTrue(self.analyzer.match(self.paste), test_hash)

        for test_hash in invalid_hashes:
            self.paste.body = test_hash
            self.assertFalse(self.analyzer.match(self.paste), test_hash)

    def test_intext(self):
        """Test if matches inside text are recognized"""
        self.paste.body = "We now have a hashe inside the text: $2a$11$EppiRqR0kG9EKy56edDWTOnsv/oGW0dqAJB9ucmn3augbmcm8v/iy and some text here!"
        self.assertTrue(self.analyzer.match(self.paste))

    def test_multiple(self):
        """Test if multiple matches are recognized"""
        self.paste.body = "We now have a hashe inside the text: $2a$11$EppiRqR0kG9EKy56edDWTOnsv/oGW0dqAJB9ucmn3augbmcm8v/iy and some text here!" \
                          "Also there is $2a$10$OyrADUFmj9QEqsd8frkEDOEYSPQalW5qoI1s2z6taCWwgUsjKzk5m as another one"
        match = self.analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual("$2a$11$EppiRqR0kG9EKy56edDWTOnsv/oGW0dqAJB9ucmn3augbmcm8v/iy", match[0])
        self.assertEqual("$2a$10$OyrADUFmj9QEqsd8frkEDOEYSPQalW5qoI1s2z6taCWwgUsjKzk5m", match[1])

    def test_match_none(self):
        """
        Matches any match * match.

        Args:
            self: (todo): write your description
        """
        self.paste.body = None
        self.assertFalse(self.analyzer.match(self.paste))

        self.paste = None
        self.assertFalse(self.analyzer.match(self.paste))

    def test_match_empty(self):
        """
        Test if the paste match.

        Args:
            self: (todo): write your description
        """
        self.paste.body = ""
        self.assertFalse(self.analyzer.match(self.paste))

    def test_actions_present(self):
        """
        Ensure that all actions have expired.

        Args:
            self: (todo): write your description
        """
        action = mock.MagicMock(spec=BasicAction)
        analyzer = BcryptHashAnalyzer(action)
        self.assertEqual([action], analyzer.actions)


if __name__ == '__main__':
    unittest.main()
