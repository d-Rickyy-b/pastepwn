# pastepwn - Paste-Scraping Python Framework

[Pastebin](https://pastebin.com) is a very helpful tool to store or rather share ascii encoded data online. In the world of OSINT, pastebin is being used by [researchers all around the world](https://www.troyhunt.com/introducing-paste-searches-and/) to retreive e.g. leaked account data, in order to find indicators about security breaches.

*Pastepwn* is a framework to scrape pastes and scan them for certain indicators. There are several analyzers and actions to be used out-of-the-box, but it is also easily extensible - you can create your own analyzers and actions on the fly.

**Please note:** This framework is **not** to be used for illegal actions. It can be used for querying public Pastebin pastes for e.g. your username or email address in order to increase your own security. 

### Setup pastepwn

To use the pastepwn framework you need to follow these simple steps:

1) **Make sure** to have a [Pastebin premium](https://pastebin.com/pro) account!
2) Install dependencies with `pip install -r requirements.txt`¹
3) Clone the repository with `git clone https://github.com/d-Rickyy-b/pastepwn.git`²
4) Create a file (e.g. `main.py`) in the project root, where you put your code in
5) Fill that file with content - add analyzers and actions. Check the [example](https://github.com/d-Rickyy-b/pastepwn/tree/master/examples/example.py) implementation.

¹ *(There will be a pypi module for installation with pip soon)*

² *(If you want to store all pastes, make sure to setup a `mongodb` instance)*


### ToDos
There are quite some features which will be implemented in the (near) future.
Check the [bug tracker](https://github.com/d-Rickyy-b/pastepwn/issues) on GitHub to get an up-to-date status about features and ToDos.

- REST API for querying paste data
- Adding more analyzers and actions, based on community input
- Adding support for other paste sites
- Add a helpful wiki with instructions and examples
