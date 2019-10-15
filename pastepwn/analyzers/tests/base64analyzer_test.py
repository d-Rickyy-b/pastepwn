# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.base64analyzer import Base64Analyzer


class TestBase64Analyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = Base64Analyzer(None)
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

        # base64 encoded string (64 chars): "Mv=ZH?NJrrBSdhus*KVg%4dG6*C&ub?sSeq!VrzCb_-QcY^KWfxKy8AJ3=^5?b6N"
        # (UTF-8, LF)
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


if __name__ == '__main__':
    unittest.main()
