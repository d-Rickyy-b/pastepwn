![Logo](https://raw.githubusercontent.com/d-Rickyy-b/pastepwn/master/documentation/pastepwn_logo.png)


# pastepwn - Paste-Scraping Python Framework
[![Build Status](https://travis-ci.com/d-Rickyy-b/pastepwn.svg?branch=master)](https://travis-ci.com/d-Rickyy-b/pastepwn)
[![PyPI version](https://badge.fury.io/py/pastepwn.svg)](https://badge.fury.io/py/pastepwn)
[![Coverage Status](https://coveralls.io/repos/github/d-Rickyy-b/pastepwn/badge.svg?branch=master)](https://coveralls.io/github/d-Rickyy-b/pastepwn?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/513ae84197824ff89c0a60a5291c4425)](https://www.codacy.com/manual/d-Rickyy-b/pastepwn?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=d-Rickyy-b/pastepwn&amp;utm_campaign=Badge_Grade)

[Pastebin](https://pastebin.com) is a very helpful tool to store or rather share ascii encoded data online. In the world of OSINT, pastebin is being used by [researchers all around the world](https://www.troyhunt.com/introducing-paste-searches-and/) to retrieve e.g. leaked account data, in order to find indicators about security breaches.

*Pastepwn* is a framework to scrape pastes and scan them for certain indicators. There are several analyzers and actions to be used out-of-the-box, but it is also easily extensible - you can create your own analyzers and actions on the fly.

**Please note:** This framework is **not** to be used for illegal actions. It can be used for querying public Pastebin pastes for e.g. your username or email address in order to increase your own security.

### ⚠️ Important note
In April 2020 Pastebin [disabled access to their scraping API](https://twitter.com/rnd_infosec_guy/status/1248310762227093509) for a short period of time. At first people weren't able to access the scraping API in any way, but later on they re-enabled access to the API setup page. But since then it isn't possible to scrape "text" pastes. Only pastes with any kind of syntax set. That reduces the amount of pastes to a minimum, which reduced the usefulness of this tool.

### Setting up pastepwn

To use the pastepwn framework you need to follow these simple steps:

1) **Make sure** to have a [Pastebin premium](https://pastebin.com/pro) account!
2) Install pastepwn via pip (`pip3 install pastepwn`)¹
3) Create a file (e.g. `main.py`) in your project root, where you put your code in²
4) Fill that file with content - add analyzers and actions. Check the [example](https://github.com/d-Rickyy-b/pastepwn/tree/master/examples/example.py) implementation.

¹ Note that pastepwn **only works with python3.6 or above**  
² *(If you want to store all pastes, make sure to set up a `mongodb`, `mysql` or `sqlite` instance)*

### Behind a proxy

There are 2 ways to use this tool behind a proxy:

- Define the following environment variables: `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY`.
- When initializing the PastePwn object, use the `proxies` argument. `proxies` is a dict as defined in [requests' documentation](http://docs.python-requests.org/en/master/user/advanced/#proxies).

### Troubleshooting
If you are having troubles, check out the [wiki pages](https://github.com/d-Rickyy-b/pastepwn/wiki) first.
If your question/issue is not resolved there, feel free to [create an issue](https://github.com/d-Rickyy-b/pastepwn/issues/new/choose) or [contact me on Telegram](https://t.me/d_Rickyy_b).

### Roadmap and ToDos
Check the [bug tracker](https://github.com/d-Rickyy-b/pastepwn/issues) on GitHub to get an up-to-date status about features and ToDos.

- REST API for querying paste data (will be another project)
- Add a helpful wiki with instructions and examples
