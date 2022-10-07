from urllib.parse import urlencode
from pastepwn.util import Request
from .basicaction import BasicAction

PASTEBIN_POST_URL = 'https://pastebin.com/api/api_post.php'

class CreatePasteAction(BasicAction):
    name = "CreatePasteAction"

    def __init__(self, dev_key, body='', title='', expire=None, syntax=None,
                 user_key='', paste_private=None):
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
        r = Request()
        response = r.post(PASTEBIN_POST_URL, data=urlencode(self.api_payload))

        if response.ok:
            return response.text
        response.raise_for_status()
