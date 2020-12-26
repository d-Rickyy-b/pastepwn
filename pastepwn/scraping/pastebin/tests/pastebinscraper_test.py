# -*- coding: utf-8 -*-
import unittest

from pastepwn.scraping.pastebin import PastebinScraper
from pastepwn.scraping.pastebin.exceptions import IPNotRegisteredError, PasteDeletedException, PasteNotReadyException, PasteEmptyException


class TestPastebinscraper(unittest.TestCase):

    def setUp(self) -> None:
        self.pastebinscraper = PastebinScraper()

    def test_empty(self):
        with self.assertRaises(PasteEmptyException):
            self.pastebinscraper._check_error("")

    def test_not_ready(self):
        with self.assertRaises(PasteNotReadyException):
            self.pastebinscraper._check_error("File is not ready for scraping yet. Try again in 1 minute.")

    def test_deleted(self):
        with self.assertRaises(PasteDeletedException):
            self.pastebinscraper._check_error("Error, we cannot find this paste.")

    def _check_ip_not_registered(self, ip_list):
        shell = "YOUR IP: {} DOES NOT HAVE ACCESS. VISIT: https://pastebin.com/doc_scraping_api TO GET ACCESS!"
        for ip in ip_list:
            with self.assertRaises(IPNotRegisteredError):
                self.pastebinscraper._check_error(shell.format(ip))
                print("The following IP was not detected: {}".format(ip))

    def test_ipv4_not_registered(self):
        """Test if the _check_error method detects different IPv4 addresses. It's okay to also detect invalid addresses where an octed is > 255)"""
        ipv4_test = ["1.1.1.1", "10.1.5.6", "1.10.5.6", "1.1.50.6", "1.1.5.60", "1.1.50.60", "1.10.50.60", "10.10.50.60", "10.10.50.255", "10.10.255.255",
                     "10.255.255.255", "255.255.255.255", "333.333.333.333"]

        self._check_ip_not_registered(ipv4_test)

    def test_ipv6_not_registered(self):
        ipv6_test = ["fe80::21d8:f50:c295:c4be", "2001:cdba:0000:0000:0000:0000:3257:9652", "2001:cdba:0:0:0:0:3257:9652", "2001:cdba::3257:9652",
                     "2001:cdba::1222", "21DA:D3:0:2F3B:2AA:FF:FE28:9C5A", "2001:cdba::1:2:3:3257:9652", "FE80::8329", "FE80::FFFF:8329",
                     "FE80::B3FF:FFFF:8329", "FE80::0202:B3FF:FFFF:8329", "FE80:0000:0000:0000:0202:B3FF:FFFF:8329"]
        # TODO: IPv6 addresses with double colon AND full zero groups (of 16 bits) are currently not recognized by the used regex. An example address would
        #  be: `FE80::0000:0000:0202:B3FF:FFFF:8329`

        self._check_ip_not_registered(ipv6_test)


if __name__ == "__main__":
    unittest.main()
