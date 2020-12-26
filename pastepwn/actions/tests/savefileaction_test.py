# -*- coding: utf-8 -*-
import os
import shutil
import unittest

from pastepwn import Paste
from pastepwn.actions.savefileaction import SaveFileAction


class TestSaveFileAction(unittest.TestCase):
    def setUp(self):
        """Setup the environment to test the action"""
        current_path = os.path.dirname(os.path.abspath(__file__))
        self.paste_path = os.path.join(current_path, "pastes")

        # Remove the directory
        try:
            shutil.rmtree(self.paste_path, ignore_errors=False)
        except FileNotFoundError:
            # Directory not there
            pass

        # Create it again
        if not os.path.exists(self.paste_path):
            os.makedirs(self.paste_path)

    def tearDown(self):
        """Reset the environment to a clean state"""
        # Remove the directory
        shutil.rmtree(self.paste_path, ignore_errors=True)

    @staticmethod
    def generate_paste():
        """Returns a paste for testing"""
        p = {"scrape_url": "https://scrape.pastebin.com/api_scrape_item.php?i=0CeaNm8Y",
             "full_url": "https://pastebin.com/0CeaNm8Y",
             "date": "1442911802",
             "key": "0CeaNm8Y",
             "size": "890",
             "expire": "1442998159",
             "title": "Once we all know when we goto function",
             "syntax": "java",
             "user": "admin",
             "body": "This is a test for pastepwn"}

        return Paste(p.get("key"), p.get("title"), p.get("user"), p.get("size"), p.get("date"), p.get("expire"), p.get("syntax"), p.get("scrape_url"),
                     p.get("full_url"))

    def test_init(self):
        """Check if initializing the action sets it up correctly"""
        template = "this is a template"
        file_ending = ".txt"
        action = SaveFileAction(self.paste_path, file_ending=file_ending, template=template)
        self.assertEqual(action.path, self.paste_path)
        self.assertEqual(action.file_ending, file_ending)
        self.assertEqual(action.template, template)

    def test_perform(self):
        """Check if storing the paste works as expected"""
        action = SaveFileAction(self.paste_path)

        paste = self.generate_paste()
        file_path = os.path.join(self.paste_path, paste.key + ".txt")

        # Perform the action == save the paste to the disk
        action.perform(paste, analyzer_name="TestSaveFileAction")

        # Make sure that the file named after the paste exists
        file_exists = os.path.exists(file_path)
        self.assertTrue(file_exists, msg="The file '{}' does not exist!".format(file_path))

        with open(file_path, "r", encoding="utf-8") as f:
            self.assertEqual(paste.body, f.read(), msg="The paste's content is different than expected!")

    def _generic_file_ending_check(self, file_ending, exp_file_ending=None):
        """Generic function to test if the files are stored with their correct file endings"""
        expected_file_ending = exp_file_ending or file_ending
        action = SaveFileAction(self.paste_path, file_ending=file_ending)
        paste = self.generate_paste()

        file_path = os.path.join(self.paste_path, paste.key + expected_file_ending)

        # Perform the action == save the paste to the disk
        action.perform(paste, analyzer_name="TestSaveFileAction")

        file_exists = os.path.exists(file_path)
        self.assertTrue(file_exists, msg="The file '{}' does not exist!".format(file_path))

    def test_other_file_ending(self):
        """Check if using another file ending works fine"""
        self._generic_file_ending_check(".yml")
        self._generic_file_ending_check(".test")
        self._generic_file_ending_check(".text")

    def test_empty_file_ending(self):
        """Check if using an empty file ending works fine"""
        self._generic_file_ending_check("")

    def test_missingdot_file_ending(self):
        """Check if using a file ending without dot works fine"""
        self._generic_file_ending_check("txt", ".txt")
        self._generic_file_ending_check("test", ".test")
        self._generic_file_ending_check("yml", ".yml")


if __name__ == "__main__":
    unittest.main()
