# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from pastepwn.analyzers.databasedumpanalyzer import DatabaseDumpAnalyzer


class TestDatabaseDumpAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = DatabaseDumpAnalyzer(None)
        self.paste = mock.Mock()

    def test_match_positive(self):
        self.paste.body = """(`id`, `team_id`, `email`, `name`, `password`, `league`, `active`, `regdate`, `lan`, `lastlogin`, `birthdate`, `favclub`, `favmanager`, `description`, `pers_email`, `mess_id`, `iso`)
                             (14, 568, 'vcpd_@hotmail.com', 'Flavio00', '059b4db7cdb1cbddc3f0e5d95c881597', 1, 1, 1224313200, 0, 0, 0, '', '', '', '', '', ''),
                             (4, 1, 'levi@medeeaweb.com', 'Slash', 'c57aeddaffce62fead6be61022eb1340', 1, 1, 1224313200, 0, 1235380637, 483260400,
                             'FC Juventus Torino', 'Carlo Ancelotti', 'I''m the admin of this site :D', 'slash@manager-arena.com', 'slashwebdesign', ''),"""
        match = self.analyzer.match(self.paste)
        self.assertTrue(match)
        self.assertEqual(1, len(match))
        self.assertEqual("""(`id`, `team_id`, `email`, `name`, `password`, `league`, `active`, `regdate`, `lan`, `lastlogin`, `birthdate`, `favclub`, `favmanager`, `description`, `pers_email`, `mess_id`, `iso`)""", match[0])


if __name__ == "__main__":
    unittest.main()
