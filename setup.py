# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

packages = find_packages()

setup(name='pastepwn',
      version='1.0.5',
      keywords='python pastebin scraping osint framework',
      description='Python framework to scrape PasteBin pastes and analyze them',
      url='https://github.com/d-Rickyy-b/pastepwn',
      author='d-Rickyy-b',
      author_email='pastepwn@rickyy.de',
      license='MIT',
      packages=packages,
      zip_safe=False)
