# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages

setup_path = os.path.dirname(os.path.abspath(__file__))
packages = find_packages(exclude=["tests*"])


# Taken from https://github.com/python-telegram-bot/python-telegram-bot/blob/9d99660ba95b103b3e1dc80414a5ce2fd805260b/setup.py#L9
def requirements():
    """Build the requirements list for this project"""
    requirements_list = []

    with open(os.path.join(setup_path, "requirements_minimum.txt")) as reqs:
        for install in reqs:
            requirements_list.append(install.strip())

        return requirements_list


with open(os.path.join(setup_path, "README.md"), "r", encoding="utf-8") as file:
    readme = file.read()

# Check if we are running on CI
CI = os.environ.get("CI")

if CI:
    version = ""
    TRAVIS_TAG = os.environ.get("TRAVIS_TAG")
    GITHUB_ACTIONS = os.environ.get("GITHUB_ACTIONS")

    if TRAVIS_TAG:
        print("Running on Travis!")
        version = TRAVIS_TAG.replace("v", "")
    elif GITHUB_ACTIONS:
        print("Running on GitHub Actions!")
        GITHUB_REF = os.environ.get("GITHUB_REF")
        tag = GITHUB_REF.split("/")[-1]
        version = tag.replace("v", "")
else:
    # Taken from https://packaging.python.org/guides/single-sourcing-package-version/
    version_dict = {}
    version_file = os.path.join(setup_path, "pastepwn", "version.py")
    with open(version_file, "r", encoding="utf-8") as file:
        exec(file.read(), version_dict)
    version = version_dict["__version__"]

print("Building version {} of pastepwn".format(version))

setup(name="pastepwn",
      version=version,
      install_requires=requirements(),
      keywords="python pastebin scraping osint framework",
      description="Python framework to scrape PasteBin pastes and analyze them",
      long_description=readme,
      long_description_content_type="text/markdown",
      url="https://github.com/d-Rickyy-b/pastepwn",
      author="d-Rickyy-b",
      author_email="pastepwn@rico-j.de",
      license="MIT",
      packages=packages,
      include_package_data=True,
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "Intended Audience :: Science/Research",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Topic :: Security",
          "Topic :: Internet",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "Programming Language :: Python :: 3.9",
          ],
      )
