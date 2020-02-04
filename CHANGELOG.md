# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased] - 2020-02-05
### Added
- Analyzers can now return a boolean or **a list of matched results**
- Actions now get passed a list of matched results by the analyzer
- New Analyzer: PasteTitleAnalyzer - Analyzer to match Paste titles via regex
- New Analyzer: IPv4AddressAnalyzer - Match IPv4 addresses via regex
- Subclasses of RegexAnalyzer now got a method `def verify(results)` that can be overwritten to filter matches so you only return valid results
- EmailPasswordPairAnalyzer has now an optional parameter `min_amount` to specify how many pairs must be found to actually match
- Base64Analyzer got an optional parameter `min_len` to specify how long a detected string must be at least to actually match
- Logical operators for analyzers - you can now connect multiple analyzers with logical operators to specify more precisely when a paste should match (aed2dbf615e7be4586747f5ea6f437663b422f57)
### Changed
- Analyzers can now return a boolean or a list of matched results
- Actions now get passed a list of matched results by the analyzer and can
- IBANAnalyzer will now filter out wrong IBANs and return a list of validated IBANs if the `validate` parameter is set to `True`
### Fixed
- Using non-capturing groups in regex for various analyzers. This is done so that the analyzer can return a matched string and at the same time it fixed some issues with analyzers not matching properly

## [1.1.0] - 2019-11-11
TBD

## [1.0.16] - 2019-09-08
### Added
- Perform checks on pastebin responses to catch errors (01f865e4acf4f7a92302a28010498732b3514d85)
- If pastes are not ready for downloading, requeue them (01f865e4acf4f7a92302a28010498732b3514d85)

## [1.0.15] - 2019-09-04
### Added
- Ability to search for multiple words in single WordAnalyzer (d2a7e0957ec1c758be2e76441e50f12b7a08a575)
- Ability to restart running scrapers after adding a new one (de99892f56e0933fee2939bac83c91fad3782994)
- Ability to register error handlers (1fae47e0b97f5d42966775d305a6b5561db1dc73)
### Fixed
- Check if paste is None before analyzing it (2fd7b398ab13c3d891b4f0164625ce38f25f205f, f4bfa466c27329839e7155b7f625ef18575ab1a8)
- Broken behaviour for WordAnalyzer blacklist (df2dd5b1627915f1b3996e7c4a10349ad837f7e2)
- Reduced sleep time in order to shut down pastepwn faster (55bb18d17ee27e443b244dcd3ea2a0362fc5853a)
- Add check in GenericAnalyzer if parameter is callable (781d6d0324fb73d93f9d8789aa08a0e72a597825)
- WordAnalyzer not matching in case sensitive mode (8762dddc2a41f01db45549006d8a9707fa1203a6)

## [1.0.14] - 2019-09-04
### Added
- Parameter for setting up storing of all downloaded pastes (e04f4761ba574df89a4972e7b88281ce57880fb0)
### Fixed
- Broken path to requirements.txt in setup.py (cc7edf41a093b1c53a9b9db309db05a19df3e44d)
- Missing column 'syntax' in sqlite table layout (3fb3821115e1973fea4af8835cfac65f48849fed)
- Broken variable substitution for sqlite statement (cf4996366cf27d7a98bfc06282e241129f771206)
- Allow writing to sqlite db from multiple threads (f47ec62cec23fa2adc1f2ed2a8fce04a9b8a041a)

## [1.0.13] - 2019-09-02
### Added
- Pastepwn got a logo! (57e6665185499b3efef8d023fd83e47c8d4cd7a6)
- Use travis tag when building pypi package (bda3c7ebba9f65ab6e469a653e835013cdf760b2)
### Fixed
- Broken paths in setup.py (42eca9bd5a21d01bd2bf1e01c074e9f2748a8948)

## [1.0.12] - 2019-02-20
### Added
- New `add_action(self, action)` method in BasicAnalyzer to add actions on the fly (4b5df12450e116a8f6754aeeacf77ba9e8efcd86)
- Created a Dockerfile (b5334ff84fae9d4d38fd11ebddfb242cd23cb893)
- Implement possibility to execute multiple actions when a paste matches (ae6055e54cb360a97547b97881fdba403e55d0e3)
- Method to create database on a mysql server (dbfecceece2f35af99fa68c5bfa67da15fa2db71)
- Stop method for pastedispatcher
- Stop method in actionhandler ()
### Changed
- Minimum supported Python version is now 3.5, because that's what we run travis on (7b8bae246522775fa2c1d1c7664612080ceddd2b)
### Fixed
- Use better sqlite create table statement (9378dadaf4bd3cbb314a2ecd2429282a72a7dad2)
- MySQL Port setting did not work (d498088b924b76d172c6602879eb9e72743ed238)
- Wrong MySQL syntax in create statements (6ae6508bc077c83ac5990839c8548749745fd75e)

## [1.0.11] - 2019-01-09
### Fixed
- Several issues with MySQL adapter (37c8f36e8603cb3f68f874a7d85d54a863c1a516)

## [1.0.10] - 2019-01-06
### Added
- Template support for Telegram messages (3f11cb5d5b4f09c9ba3ea49c1b9aa120d9d6a87f)
### Fixed
- Travis config for pypi (c2608a0b70e1bb5d4759759a0db77254f02dfebd)
- Wrong MySQL syntax in create statement (b3afc3d0734ad104d29612c404254e79ce28e5c6)

## [1.0.9-travis] - 2018-10-26
### Added
- Travis badge in Readme
- Usage description in Readme

## [1.0.8-travis] - 2018-10-26
### Added
- Travis config file (dd3db552a03c40bde3ae2a149d2844a60f886417)

## [1.0.8] - 2018-10-22
First stable release

[unreleased]: https://github.com/d-Rickyy-b/pastepwn/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/d-Rickyy-b/pastepwn/compare/v1.0.16...v1.1.0
[1.0.16]: https://github.com/d-Rickyy-b/pastepwn/compare/v1.0.15...v1.0.16
[1.0.15]: https://github.com/d-Rickyy-b/pastepwn/compare/v1.0.14...v1.0.15
[1.0.14]: https://github.com/d-Rickyy-b/pastepwn/compare/v1.0.13...v1.0.14
[1.0.13]: https://github.com/d-Rickyy-b/pastepwn/compare/v1.0.12...v1.0.13
[1.0.12]: https://github.com/d-Rickyy-b/pastepwn/compare/v1.0.11...v1.0.12
[1.0.11]: https://github.com/d-Rickyy-b/pastepwn/compare/v1.0.10...v1.0.11
[1.0.10]: https://github.com/d-Rickyy-b/pastepwn/compare/v1.0.9-travis...v1.0.10
[1.0.9-travis]: https://github.com/d-Rickyy-b/pastepwn/compare/v1.0.8-travis...v1.0.9-travis
[1.0.8-travis]: https://github.com/d-Rickyy-b/pastepwn/compare/v1.0.8...v1.0.8-travis
[1.0.8]: https://github.com/d-Rickyy-b/pastepwn/tree/v1.0.8
