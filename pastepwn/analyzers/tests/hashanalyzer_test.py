# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.hashanalyzer import HashAnalyzer


class TestHashAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = HashAnalyzer(None, [
            b"hunter2",
            b"SuperSecurePassword!123",
            b""
            ])
        self.paste = mock.Mock()

    def test_match(self):
        md5_hashes = ["2ab96390c7dbe3439de74d0c9b0b1767",
                      "0fceb0a9f3d9e4a454df92965c7d9f3e",
                      "d41d8cd98f00b204e9800998ecf8427e"
                      ]
        sha1_hashes = ["f3bbbd66a63d4bf1747940578ec3d0103530e21d",
                       "1a0f39c3bdc08e7e3bb6f02ed181ad96ee90f766",
                       "da39a3ee5e6b4b0d3255bfef95601890afd80709"
                       ]
        sha256_hashes = ["f52fbd32b2b3b86ff88ef6c490628285f482af15ddcb29541f94bcf526a3f6c7",
                         "4bf33443cc946e7ef2b394f6874a74113c7b7b142765afcdfca142ad32a1bf1e",
                         "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
                         ]

        invalid_hashes = ["9f9d51bc70ef21ca5c14f307980a29d8",
                          "5f4dcc3b5aa765d61d8327deb882cf99",
                          "81b637d8fcd2c6da6359e6963113a1170de795e4b725b84d1e0b4cfd9ec58ce9",
                          "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
                          ]

        for test_hash in (md5_hashes + sha1_hashes + sha256_hashes):
            self.paste.body = test_hash
            self.assertTrue(self.analyzer.match(self.paste), test_hash)

        for test_hash in invalid_hashes:
            self.paste.body = test_hash
            self.assertFalse(self.analyzer.match(self.paste), test_hash)

    def test_match_case_insensitive(self):
        self.paste.body = "2ab96390c7dbe3439de74d0c9b0b1767"
        self.assertTrue(self.analyzer.match(self.paste), "lowercase hash")
        self.paste.body = "2AB96390C7DBE3439DE74D0C9B0B1767"
        self.assertTrue(self.analyzer.match(self.paste), "uppercase hash")

    def test_match_md5_only(self):
        md5_analyzer = HashAnalyzer(None, [b"hunter2", b"SuperSecurePassword!123", b""], ["md5"])
        self.paste.body = "0fceb0a9f3d9e4a454df92965c7d9f3e"
        self.assertTrue(md5_analyzer.match(self.paste), "MD5 hash")
        self.paste.body = "1a0f39c3bdc08e7e3bb6f02ed181ad96ee90f766"
        self.assertFalse(md5_analyzer.match(self.paste), "SHA-1 hash")

    def test_unavailable_algorithms(self):
        with self.assertRaises(ValueError):
            HashAnalyzer(None, [b"hunter2"], ["super_algorithm_not_available"])

    def test_single_password_input(self):
        single_password_analyzer = HashAnalyzer(None, b"hunter2")
        self.paste.body = "f52fbd32b2b3b86ff88ef6c490628285f482af15ddcb29541f94bcf526a3f6c7"
        self.assertTrue(single_password_analyzer.match(self.paste), "SHA-256 hash")
        self.paste.body = "aaa9402664f1a41f40ebbc52c9993eb66aeb366602958fdfaa283b71e64db123"
        self.assertFalse(single_password_analyzer.match(self.paste), "SHA-256 hash of 'h'")
