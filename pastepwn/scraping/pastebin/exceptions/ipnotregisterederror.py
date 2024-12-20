class IPNotRegisteredError(Exception):
    """Exception class indicating that your IP is not witelisted on pastebin"""

    def __init__(self, ip_address):
        super().__init__(f"The IP you use for scraping ({ip_address}) was not whitelisted. Visit https://pastebin.com/doc_scraping_api to get access!")
