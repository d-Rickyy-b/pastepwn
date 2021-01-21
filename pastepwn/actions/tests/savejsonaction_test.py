# -*- coding: utf-8 -*-

import unittest
from unittest.mock import Mock, patch

from pastepwn.actions import SaveJSONAction


class TestSaveJSONAction(unittest.TestCase):

    def setUp(self):
        """Sets up the test case"""
        self.action = SaveJSONAction(path="")
        self.paste = Mock()
        self.path_mock = Mock()
        self.path_mock.__truediv__ = Mock(side_effect=self.side_effect)
        self.path_mock.exists = Mock(return_value=True)

    @staticmethod
    def side_effect(path):
        return path

    def test_get_file_content(self):
        """Check if the content of the file is returned correctly"""
        self.paste.to_dict = Mock(return_value={"test": "content", "another": "item"})
        content_string = """{"test": "content", "another": "item"}"""
        content = self.action.get_file_content(self.paste, "", [])
        self.assertEqual(content_string, content)

    @patch("builtins.open")
    @patch("pastepwn.actions.savejsonaction.json")
    def test_file_ending(self, json_mock, open_mock):
        """Check that the file ending is actually json, not txt"""
        json_mock.dumps = Mock(return_value="json content!")

        self.action.path = self.path_mock

        self.paste.key = Mock()
        self.paste.key.__repr__ = Mock(return_value="123456")
        self.action.perform(self.paste)

        open_mock.assert_called_with("123456.json", "w", encoding="utf-8")
        open_mock().__enter__().write.assert_called_with("json content!")


if __name__ == "__main__":
    unittest.main()
