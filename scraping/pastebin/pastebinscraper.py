# -*- coding: utf-8 -*-
import json
# https://pastebin.com/doc_scraping_api#2
# Your whitelisted IP should not run into any issues as long as you don't abuse our service.
# We recommend not making more than 1 request per second, as there really is no need to do so.
# Going over 1 request per second won't get you blocked, but if we see excessive unnecessary scraping, we might take action.

api_base_url = "https://scrape.pastebin.com/"


def check_error(body):
    """Checks and returns True if an error occurred"""
    if "DOES NOT HAVE ACCESS" in body:
        return True


def get_recent(limit=10):
    endpoint = "api_scraping.php"
    api_url = api_base_url + endpoint

    try:
        pass
        # Send request to pastebin
        # Check for errors
        # Load json to dict | json.loads()
    except:
        pass

    # return dict


def get_paste(key):
    endpoint = "api_scrape_item.php"
    api_url = api_base_url + endpoint
    paste = None

    try:
        pass
        # fetch content
    except:
        pass

    return paste



# Error message:
# YOUR IP: xxx.xxx.xxx.xxx DOES NOT HAVE ACCESS.
#
# VISIT: https://pastebin.com/doc_scraping_api TO GET ACCESS!