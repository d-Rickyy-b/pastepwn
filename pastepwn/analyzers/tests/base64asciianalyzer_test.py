# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.base64asciianalyzer import Base64AsciiAnalyzer


class TestBase64AsciiAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = Base64AsciiAnalyzer(None)
        self.paste = mock.Mock()

    def test_match_positive(self):
        """Test if positives are recognized"""
        # base64 encoded string: "Hello World" (UTF-8, LF)
        self.paste.body = "SGVsbG8gV29ybGQ="
        self.assertTrue(self.analyzer.match(self.paste))

        # base64 encoded string: "Hello\nWorld" (UTF-8, LF)
        self.paste.body = "SGVsbG9cbldvcmxk"
        self.assertTrue(self.analyzer.match(self.paste))

        # base64 encoded string (32 chars): "2fwZ_CTjDKxu48FLCLZcGdB!sEj5XRQh" (UTF-8, LF)
        self.paste.body = "MmZ3Wl9DVGpES3h1NDhGTENMWmNHZEIhc0VqNVhSUWg="
        self.assertTrue(self.analyzer.match(self.paste))

        # base64 encoded string (64 chars): "Mv=ZH?NJrrBSdhus*KVg%4dG6*C&ub?sSeq!VrzCb_-QcY^KWfxKy8AJ3=^5?b6N" (UTF-8, LF)
        self.paste.body = "TXY9Wkg/TkpyckJTZGh1cypLVmclNGRHNipDJnViP3NTZXEhVnJ6Q2JfLVFjWV5LV2Z4S3k4QUozPV41P2I2Tg=="
        self.assertTrue(self.analyzer.match(self.paste))

        # base64 encoded string (256 chars): "etFk!?m@A_vvdMT39Mgcynx_AFz6HY!4R8U3n_7JA?-rF=F3ehWat%4rKfhsuCc98G
        # =t8jMY7hgJDZ2c!y!$!XQATbk6fQD2pa+EdQ_rfP^&_DKJ34dFPcuGjDBTqdxZ&=3U%@dm&?JW#+k@mB%a3TFn%GAzukL+-%TUTq?fAbAKr
        # @y%LPK+KEmxeh+rg7?s3aR2v5A%tbn&_7zNMckCPRd&s8$wW5Bec@aRMCs@4rn?cRx?a&y-Z%kn&h8aLu*R" (UTF-8, LF)
        self.paste.body = "ZXRGayE/bUBBX3Z2ZE1UMzlNZ2N5bnhfQUZ6NkhZITRSOFUzbl83SkE/LXJGPUYzZWhXYXQlNHJLZmhzdUNjO" \
                          "ThHPXQ4ak1ZN2hnSkRaMmMheSEkIVhRQVRiazZmUUQycGErRWRRX3JmUF4mX0RLSjM0ZEZQY3VHakRCVHFkeF" \
                          "omPTNVJUBkbSY/SlcjK2tAbUIlYTNURm4lR0F6dWtMKy0lVFVUcT9mQWJBS3JAeSVMUEsrS0VteGVoK3JnNz9" \
                          "zM2FSMnY1QSV0Ym4mXzd6Tk1ja0NQUmQmczgkd1c1QmVjQGFSTUNzQDRybj9jUng/YSZ5LVola24maDhhTHUqUg=="
        self.assertTrue(self.analyzer.match(self.paste))

    def test_intext(self):
        """Test if matches inside text are recognized"""
        self.paste.body = "I wan to tel you tha TXY9Wkg/TkpyckJTZGh1cypLVmclNGRHNipDJnViP3NTZXEhVnJ6Q2JfLVFjWV5LV2Z4S3k4QUozPV41P2I2Tg== is " \
                          "very important"
        match = self.analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual("TXY9Wkg/TkpyckJTZGh1cypLVmclNGRHNipDJnViP3NTZXEhVnJ6Q2JfLVFjWV5LV2Z4S3k4QUozPV41P2I2Tg==", match[0])

    def test_multiple(self):
        """Test if multiple matches are recognized"""
        # Needed to keep the words below 3 chars each. Otherwise they would match as well
        self.paste.body = "I wan to tel you tha TXY9Wkg/TkpyckJTZGh1cypLVmclNGRHNipDJnViP3NTZXEhVnJ6Q2JfLVFjWV5LV2Z4S3k4QUozPV41P2I2Tg== is " \
                          "ver imp.\nBut not onl tha, it's als MmZ3Wl9DVGpES3h1NDhGTENMWmNHZEIhc0VqNVhSUWg= and muc mor!"
        match = self.analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual("TXY9Wkg/TkpyckJTZGh1cypLVmclNGRHNipDJnViP3NTZXEhVnJ6Q2JfLVFjWV5LV2Z4S3k4QUozPV41P2I2Tg==", match[0])
        self.assertEqual("MmZ3Wl9DVGpES3h1NDhGTENMWmNHZEIhc0VqNVhSUWg=", match[1])

    def test_multiple_min_len(self):
        """Test if we can match multiple base64 strings in a longer text with min_len"""
        analyzer = Base64AsciiAnalyzer(None, min_len=8)
        self.paste.body = "I wanted to tell you that TXY9Wkg/TkpyckJTZGh1cypLVmclNGRHNipDJnViP3NTZXEhVnJ6Q2JfLVFjWV5LV2Z4S3k4QUozPV41P2I2Tg== is " \
                          "very important.\nBut not only that, it's also MmZ3Wl9DVGpES3h1NDhGTENMWmNHZEIhc0VqNVhSUWg= and much more!"
        match = analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual("TXY9Wkg/TkpyckJTZGh1cypLVmclNGRHNipDJnViP3NTZXEhVnJ6Q2JfLVFjWV5LV2Z4S3k4QUozPV41P2I2Tg==", match[0])
        self.assertEqual("MmZ3Wl9DVGpES3h1NDhGTENMWmNHZEIhc0VqNVhSUWg=", match[1])

    def test_min_len(self):
        """Test if the min_len parameter works as expected"""
        self.paste.body = "dGVz"
        analyzer = Base64AsciiAnalyzer(None, min_len=4)
        match = analyzer.match(self.paste)
        self.assertTrue(match)

        self.paste.body = "dGVz"
        analyzer = Base64AsciiAnalyzer(None, min_len=5)
        match = analyzer.match(self.paste)
        self.assertFalse(match)

        self.paste.body = "dGVzdFRoaXNTdHJpbmc="
        match = analyzer.match(self.paste)
        self.assertTrue(match)

    def test_match_negative(self):
        """Test if negatives are not recognized"""
        # test that when nothing, is provided nothing matches
        self.paste.body = ""
        self.assertFalse(self.analyzer.match(self.paste))

        # test that when nothing, is provided nothing matches
        self.paste.body = None
        self.assertFalse(self.analyzer.match(self.paste))

        # invalid base64 string (% symbol inserted which is not valid base64)
        self.paste.body = "SGVsbG8gV%29ybGQ="
        self.assertFalse(self.analyzer.match(self.paste))

        # not a base64 string
        self.paste.body = "====="
        self.assertFalse(self.analyzer.match(self.paste))

        # base32 encoded string
        self.paste.body = "JBSWY3DPEBLW64TMMQ======"
        self.assertFalse(self.analyzer.match(self.paste))

        # long string (129) not base64
        self.paste.body = "sFm2XgxTt6fuErnWw9JZkae76sL7XDqyNvf2Wkatt9gkzVDxXTf6dCr3Yh6fT82fFzvNWG49P3KSR7XXngHJ5D9ba" \
                          "Dj448rhbNTJrKhRn7TPkYRubZLhmbCrg6bavDa9a"
        self.assertFalse(self.analyzer.match(self.paste))

    def test_invalid_decodes(self):
        """Test to make sure we don't match base64 strings which don't decode to ASCII"""
        # base64 encoded string containing one non-ascii character: "This string contains a non-ascii character: ¤" (UTF-8)
        self.paste.body = "VGhpcyBzdHJpbmcgY29udGFpbnMgYSBub24tYXNjaWkgY2hhcmFjdGVyOiDCpA=="
        self.assertFalse(self.analyzer.match(self.paste))

        # base64 encoded string containing only non-ascii characters: "ΗÈλλθ ωÖΓλÐ" (UTF-8)
        self.paste.body = "zpfDiM67zrvOuCDPicOWzpPOu8OQ"
        self.assertFalse(self.analyzer.match(self.paste))

        # base64 encoded string containing one non-ascii character: "º" (UTF-8)
        self.paste.body = "wro="
        self.assertFalse(self.analyzer.match(self.paste))

    def test_ascii_decode(self):
        """Test if ascii decode flag works"""
        analyzer = Base64AsciiAnalyzer(None, decode=True)

        # base64 encoded string: "Hello World" (UTF-8, LF)
        self.paste.body = "SGVsbG8gV29ybGQ="
        self.assertEqual("Hello World", analyzer.match(self.paste)[0])

        # base64 encoded string: "Hello\nWorld" (UTF-8, LF)
        self.paste.body = "SGVsbG8KV29ybGQ="
        self.assertEqual("Hello\nWorld", analyzer.match(self.paste)[0])

        # base64 encoded string (32 chars): "2fwZ_CTjDKxu48FLCLZcGdB!sEj5XRQh" (UTF-8, LF)
        self.paste.body = "MmZ3Wl9DVGpES3h1NDhGTENMWmNHZEIhc0VqNVhSUWg="
        self.assertEqual("2fwZ_CTjDKxu48FLCLZcGdB!sEj5XRQh", analyzer.match(self.paste)[0])

        # base64 encoded string (64 chars): "Mv=ZH?NJrrBSdhus*KVg%4dG6*C&ub?sSeq!VrzCb_-QcY^KWfxKy8AJ3=^5?b6N" (UTF-8, LF)
        self.paste.body = "TXY9Wkg/TkpyckJTZGh1cypLVmclNGRHNipDJnViP3NTZXEhVnJ6Q2JfLVFjWV5LV2Z4S3k4QUozPV41P2I2Tg=="
        self.assertEqual("Mv=ZH?NJrrBSdhus*KVg%4dG6*C&ub?sSeq!VrzCb_-QcY^KWfxKy8AJ3=^5?b6N", analyzer.match(self.paste)[0])

        # base64 encoded string (256 chars): "etFk!?m@A_vvdMT39Mgcynx_AFz6HY!4R8U3n_7JA?-rF=F3ehWat%4rKfhsuCc98G
        # =t8jMY7hgJDZ2c!y!$!XQATbk6fQD2pa+EdQ_rfP^&_DKJ34dFPcuGjDBTqdxZ&=3U%@dm&?JW#+k@mB%a3TFn%GAzukL+-%TUTq?fAbAKr
        # @y%LPK+KEmxeh+rg7?s3aR2v5A%tbn&_7zNMckCPRd&s8$wW5Bec@aRMCs@4rn?cRx?a&y-Z%kn&h8aLu*R" (UTF-8, LF)
        self.paste.body = "ZXRGayE/bUBBX3Z2ZE1UMzlNZ2N5bnhfQUZ6NkhZITRSOFUzbl83SkE/LXJGPUYzZWhXYXQlNHJLZmhzdUNjO" \
                          "ThHPXQ4ak1ZN2hnSkRaMmMheSEkIVhRQVRiazZmUUQycGErRWRRX3JmUF4mX0RLSjM0ZEZQY3VHakRCVHFkeF" \
                          "omPTNVJUBkbSY/SlcjK2tAbUIlYTNURm4lR0F6dWtMKy0lVFVUcT9mQWJBS3JAeSVMUEsrS0VteGVoK3JnNz9" \
                          "zM2FSMnY1QSV0Ym4mXzd6Tk1ja0NQUmQmczgkd1c1QmVjQGFSTUNzQDRybj9jUng/YSZ5LVola24maDhhTHUqUg=="
        self.assertEqual("etFk!?m@A_vvdMT39Mgcynx_AFz6HY!4R8U3n_7JA?-rF=F3ehWat%4rKfhsuCc98G"
                         "=t8jMY7hgJDZ2c!y!$!XQATbk6fQD2pa+EdQ_rfP^&_DKJ34dFPcuGjDBTqdxZ&=3U%"
                         "@dm&?JW#+k@mB%a3TFn%GAzukL+-%TUTq?fAbAKr@y%LPK+KEmxeh+rg7?s3aR2v5A%tbn&"
                         "_7zNMckCPRd&s8$wW5Bec@aRMCs@4rn?cRx?a&y-Z%kn&h8aLu*R", analyzer.match(self.paste)[0]
                         )


if __name__ == "__main__":
    unittest.main()
