# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

packages = find_packages()


# Taken from https://github.com/python-telegram-bot/python-telegram-bot/blob/9d99660ba95b103b3e1dc80414a5ce2fd805260b/setup.py#L9
def requirements():
    """Build the requirements list for this project"""
    requirements_list = []

    with open('requirements.txt') as reqs:
        for install in reqs:
            requirements_list.append(install.strip())

        return requirements_list


setup(name='pastepwn',
      version='1.0.6',
      install_requires=requirements(),
      keywords='python pastebin scraping osint framework',
      description='Python framework to scrape PasteBin pastes and analyze them',
      url='https://github.com/d-Rickyy-b/pastepwn',
      author='d-Rickyy-b',
      author_email='pastepwn@rickyy.de',
      license='MIT',
      packages=packages,
      zip_safe=False)
