# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock, patch

from pastepwn.actions.savefileaction import SaveFileAction


class TestSaveFileAction(unittest.TestCase):

    def setUp(self):
        """Sets up the test case"""
        self.action = SaveFileAction(path="")
        self.paste = Mock()
        self.path_mock = Mock()
        self.path_mock.__truediv__ = Mock(side_effect=self.side_effect)
        self.path_mock.exists = Mock(return_value=True)

    @staticmethod
    def side_effect(path):
        return path

    def test_init(self):
        """Check if parameters are saved correctly"""
        self.action = SaveFileAction(path="/this/is/a/test")
        self.assertEqual("/this/is/a/test", self.action.path.as_posix())

        self.action = SaveFileAction(path="Test")
        self.assertEqual("Test", self.action.path.as_posix())

        # Check if multiple values for init are stored correctly
        self.action = SaveFileAction(path="/test", file_ending=".txt", template="Template string")
        self.assertEqual("/test", self.action.path.as_posix())
        self.assertEqual(".txt", self.action.file_ending)
        self.assertEqual("Template string", self.action.template)

        # Check if
        self.action = SaveFileAction(path="/test")
        self.assertEqual(".txt", self.action.file_ending)
        self.assertEqual("${body}", self.action.template)

    @patch("builtins.open")
    @patch("pastepwn.actions.savefileaction.TemplatingEngine")
    def test_perform_path_not_exists(self, te_mock, open_mock):
        """Check if calling perform with non existing path works as intended."""
        te_mock.fill_template = Mock(return_value="This is some content")

        # Mock pathlib to be independent of filesystem for this test
        self.path_mock.exists = Mock(return_value=False)
        self.action.path = self.path_mock

        # We need to make sure that the file's name is the key
        self.paste.key = "thisIsTheRythmOfTheFile"

        self.action.perform(self.paste, "", [])

        # Since the path didn't exist, we must have called "mkdir" once
        self.action.path.mkdir.assert_called_once_with(parents=True, exist_ok=True)

        # fill_template must be called for the perform method
        te_mock.fill_template.assert_called_once()

        # Make sure that the file was opened and written
        open_mock.assert_called_with("thisIsTheRythmOfTheFile.txt", "w", encoding="utf-8")
        open_mock().__enter__().write.assert_called_with("This is some content")

    @patch("builtins.open")
    @patch("pastepwn.actions.savefileaction.TemplatingEngine")
    def test_perform_path_exists(self, te_mock, open_mock):
        """Check if calling perform with non existing path works as intended."""
        te_mock.fill_template = Mock(return_value="Some other content")

        # Mock pathlib to be independent of filesystem and write rights for this test
        self.action.path = self.path_mock

        # We need to make sure that the file's name is the key
        self.paste.key = "myFile"

        self.action.perform(self.paste, "", [])

        # Since the path did exist, we mustn't call "mkdir"
        self.action.path.mkdir.assert_not_called()

        # fill_template must be called for the perform method
        te_mock.fill_template.assert_called_once()

        # Make sure that the file was opened and written
        open_mock.assert_called_with("myFile.txt", "w", encoding="utf-8")
        open_mock().__enter__().write.assert_called_with("Some other content")

    @patch("builtins.open")
    @patch("pastepwn.actions.savefileaction.TemplatingEngine")
    def test_perform_file_ending_empty(self, te_mock, open_mock):
        """Check if calling perform with non existing path works as intended."""
        te_mock.fill_template = Mock(return_value="Again another content")

        # Mock pathlib to be independent of filesystem and write rights for this test
        self.action.path = self.path_mock
        self.action.file_ending = ""

        # We need to make sure that the file's name is the key
        file_name = "nameOfAFile"
        self.paste.key = Mock()
        self.paste.key.__repr__ = Mock(return_value=file_name)

        self.action.perform(self.paste, "", [])

        # Since the path did exist, we mustn't call "mkdir"
        self.action.path.mkdir.assert_not_called()

        # fill_template must be called for the perform method
        te_mock.fill_template.assert_called_once()

        # We called str(paste.key) once
        self.paste.key.__repr__.assert_called_once()

        # Make sure that the file was opened and written
        open_mock.assert_called_with(file_name, "w", encoding="utf-8")
        open_mock().__enter__().write.assert_called_with("Again another content")

    @patch("builtins.open")
    @patch("pastepwn.actions.savefileaction.TemplatingEngine")
    def test_perform_file_ending(self, te_mock, open_mock):
        """Check if calling perform with non existing path works as intended."""
        te_mock.fill_template = Mock(return_value="This is some content")

        self.action.path = self.path_mock
        self.action.file_ending = ".asdf"

        # We need to make sure that the file's name is the key
        self.paste.key = Mock()
        self.paste.key.__repr__ = Mock(return_value="123456")

        self.action.perform(self.paste, "", [])

        self.action.path.mkdir.assert_not_called()
        te_mock.fill_template.assert_called_once()
        self.paste.key.__repr__.assert_called_once()

        # Make sure that the file was opened and written
        open_mock.assert_called_with("123456.asdf", "w", encoding="utf-8")
        open_mock().__enter__().write.assert_called_with("This is some content")

    @patch("pastepwn.actions.savefileaction.TemplatingEngine")
    def test_get_file_content(self, te_mock):
        """Check if the content of the file is returned correctly"""
        te_mock.fill_template = Mock(return_value="This is the content")
        content = self.action.get_file_content(self.paste, "", [])
        self.assertEqual("This is the content", content)

    def test__remove_prefix(self):
        """Check if removing prefixes from a string works fine."""
        input_string = ".txt"
        prefix = "."
        res = self.action._remove_prefix(input_string, prefix)
        self.assertEqual("txt", res)

        input_string = ".json"
        prefix = "."
        res = self.action._remove_prefix(input_string, prefix)
        self.assertEqual("json", res)

        input_string = ".txt"
        prefix = "_"
        res = self.action._remove_prefix(input_string, prefix)
        self.assertEqual(".txt", res)

        input_string = ""
        prefix = "."
        res = self.action._remove_prefix(input_string, prefix)
        self.assertEqual("", res)

        input_string = "..txt"
        prefix = "."
        res = self.action._remove_prefix(input_string, prefix)
        self.assertEqual(".txt", res)

        input_string = ".txt."
        prefix = "."
        res = self.action._remove_prefix(input_string, prefix)
        self.assertEqual("txt.", res)

        input_string = "This is a very long string without prefix"
        prefix = "A"
        res = self.action._remove_prefix(input_string, prefix)
        self.assertEqual("This is a very long string without prefix", res)

        input_string = "AAABBBCCC"
        prefix = "A"
        res = self.action._remove_prefix(input_string, prefix)
        self.assertEqual("AABBBCCC", res)


if __name__ == "__main__":
    unittest.main()
