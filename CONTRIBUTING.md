# Contributing

Want to contribute? Developers of any skill level can find opportunities to contribute. Bug reports, fixes, documentation improvements, enhancements, and ideas are all welcome! 

## Where to begin?

If you are new to *Pastepwn* or open-source development in general, checking out the [Github "Issues" tab](https://github.com/d-Rickyy-b/pastepwn/issues) is recommended. There, you can find everything from bugs in need of fixes to requests for documentation and more.

For newer developers, it's recommended to start with issues with the labels, **"Difficulty: Easy"** and/or **"good first issue"**.

## Reporting bugs and requesting enhancements

If you have discovered a bug or want to request an enhancement, you will need to create a **New Issue** in [the "Issues" tab](https://github.com/d-Rickyy-b/pastepwn/issues). You may also want to [reach out on Telegram](https://t.me/d_Rickyy_b).

### Preparing a bug report

In order to best fix a bug, it's key for other developers to be able to reproduce it. A great bug report can help that bug be reproducible! For tips on writing a good bug report, check out [this stackoverflow article](https://stackoverflow.com/help/minimal-reproducible-example). 

In short, please try to include the following:

1. A short snippet of code that incited the bug. Formatting the code using [Github Markdown](https://docs.github.com/en/github/writing-on-github) would also be helpful.
2. An explanation of why the behavior is incorrect and what you expected.

## Getting assigned an issue

Found an issue you'd like to resolve? Great! If the issue has not already been claimed by another developer, write out a comment expressing your interest in claiming the issue and resolving it.

## Editing the code

Whether you want to fix a bug, add an enhancement, or improve the documentation, you will need to know your way around Git and Github. 

*Pastepwn* is hosted on Github, so ensure you've brushed up on the [the basics](https://docs.github.com/en/get-started). Also ensure you understand Git, which Github is built upon, by [setting it up](https://docs.github.com/en/get-started/quickstart/set-up-git) and learning the ropes.

Other requirements:

* [Python](https://www.python.org/downloads/) ver. 3.6 or greater
* A [Pastebin Premium](https://pastebin.com/pro) account for testing/changing paste scrapping and scanning functionality
* [Docker Desktop](https://www.docker.com/products/docker-desktop) and [Docker-compose](https://docs.docker.com/compose/install/) if working via Docker and using a [MySQL Database](https://github.com/d-Rickyy-b/pastepwn/wiki/MySQL-Database-Setup)
* Familiarity with everything explained in the [README](https://github.com/d-Rickyy-b/pastepwn/blob/master/README.md) and [Wiki](https://github.com/d-Rickyy-b/pastepwn/wiki)
* Download the required dependencies with the below command line in the *Pastepwn* root directory:

```
pip install -r requirements.txt
```

### Forking a repository

You will need to fork your own repository to be able to edit the source code. On the *Pastepwn* Github page, click on the Fork button. After forking and cloning your *Pastepwn* repository, make sure you run the following command line in the root directory of your clone:
```
git remote add upstream https://github.com/d-Rickyy-b/pastepwn.git
```
This will connect your repository to the main *Pastepwn* repository and will be helpful with setting up your pull request later.

### Style guide

*Pastepwn* uses flake8 to ensure properly styled "Pythonic" code that corresponds to the official PEP 8 standard. Make sure you install it via the below command line in the *Pastepwn* root directory:

```
pip install -r requirements_flake8.txt
```

Then, to have your code style checked, run the following command line, subbing in the name of the root directory for your local *Pastepwn* repository:
```
flake8 your_pastepwn_directory
```

## Contributing your changes

Once you have your edited code ready to be contributed to the main *Pastepwn* respository, you still have a few steps to tackle!

### Writing a commit

After adding your changed files to your Git, it's time to commit your changes to your local repository with an explanatory message. The general structure of a commit message is based off of **Conventional Commits** and should match the following:
```
<type>[optional scope]: <description>

[optional body]

[optional footer]
```
For example, the commit message for an edit to the documentation may look something like this:
```
docs: correct spelling of CONTRIBUTING
```
For a more detailed view of this commit writing structure, please visit [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0-beta.4/).

### Making a pull request

Once you have pushed your the changed files to your repository on Github, it is time to make a pull request. 

1. Click the **Pull request** button on your Github repository
2. Review your code by clicking **Commits** and **Files Changed**
3. Write a description of your changes in the **Preview Discussion** tab that matches up with your commit messages
4. Click **Send Pull Request**

This request will go to the main repository developer and will be reviewed by them. If all goes well, congrats!

## Understanding versioning

Lastly, it is worth pointing out and understanding how *Pastepwn* handles versioning. *Pastepwn* follows the **Semantic Versioning** standard for how release versions are handled, which also requires a [Changelog](https://keepachangelog.com/en/1.0.0/) noting all changes made with each new version release. For a better understand it, please visit the [Semantic Versioning site](https://semver.org/). 
