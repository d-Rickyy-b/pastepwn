

class IPNotRegisteredError(Exception):
    """Exception class indicating that your IP is not witelisted on pastebin"""

    def __init__(self, ip_address):
        super().__init__("The IP you use for scraping ({0}) was not whitelisted. Visit https://pastebin.com/doc_scraping_api to get access!".format(ip_address))
