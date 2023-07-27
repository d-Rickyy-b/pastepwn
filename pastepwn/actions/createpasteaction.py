from urllib.parse import urlencode
from pastepwn.util import Request
from .basicaction import BasicAction

PASTEBIN_POST_URL = 'https://pastebin.com/api/api_post.php'

class CreatePasteAction(BasicAction):
    """
    Action to create a new Paste with custom content on Pastebin.
    API Doc: https://pastebin.com/doc_api#2
    """
    name = "CreatePasteAction"

    def __init__(self, dev_key, body='', title='', expire=None, syntax=None,
                 user_key='', paste_private=None):
        """
        Action to create a new paste on Pastebin.
        :param dev_key: The API Developer Key of a registered U{http://pastebin.com} account.
        :param body: The String to paste to body of the U{http://pastebin.com} paste.
        :param title: Title of the paste.
        :param expire: New paste expiration date.
        :param syntax: Programming language of the code being pasted.
        :param user_key: The API User Key of a U{http://pastebin.com} registered user.
        :param paste_private: Possible values: 'public', 'unlisted' and 'private'.

        Contructs the payload required for the API.
        """
        super().__init__()
        paste_priv_rel = {
            'public': 0,
            'unlisted': 1,
            'private': 2
        }

        self.api_payload = {'api_dev_key': dev_key,
                         'api_paste_code': body,
                         'api_paste_name': title,
                         'api_option': 'paste',
                         'api_user_key': user_key
                        }

        if expire:
            self.api_payload['api_paste_expire_date'] = str(expire).strip().upper()

        if syntax:
            self.api_payload['api_paste_format'] = str(syntax).strip().lower()

        if paste_private:
            self.api_payload['api_paste_private'] = paste_priv_rel.get(paste_private.strip().lower(), 0)


    def perform(self, paste, analyzer_name=None, matches=None):
        """
        Performs a POST request to Pastebin with the constructed payload.
        :param paste: The paste passed by the ActionHandler
        :param analyzer_name: The name of the analyzer which matched the paste
        :param matches: List of matches returned by the analyzer
        :return str: URL of the newly generated paste if successful else raises an exception."""
        r = Request()
        response = r.post(PASTEBIN_POST_URL, data=urlencode(self.api_payload))

        if response.ok:
            return response.text
        response.raise_for_status()
