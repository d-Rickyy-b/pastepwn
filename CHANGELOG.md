# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Implemented ExactWordAnalyzer to match words exactly rather than partially ([08ebdbc](https://github.com/d-Rickyy-b/pastepwn/commits/08ebdbc3fb5c8431486f8367e039e8580c67770a))

## [1.3.1] - 2020-06-20
### Fixed
- The PastebinScraper could not recognize error messages with IPv6 addresses.

### Docs
- Started adding some readme files for the subfolders to explain certain parts of the code better 

## [1.3.0] - 2020-03-03
### Added
- Implemented base64analyzer, which matches if a found base64 string decodes to valid ascii ([b535781](https://github.com/d-Rickyy-b/pastepwn/commit/b535781d7e1760c7f846432d7ef87b97784e2d49))
- Implemented IrcAction - the previous implementation was not working ([546b87f](https://github.com/d-Rickyy-b/pastepwn/commit/546b87f508420da0a9ea6f54f1df65684b73648f))
### Changed
- SaveFileAction now got a parameter to set the file ending and a template ([c3d75f7](https://github.com/d-Rickyy-b/pastepwn/commit/c3d75f72036fa1284eebc8f3c1967a4374428dca))
### Fixed
- Analyzers now check if a passed action is a subclass of BasicAction, which prevents issues such as [#175](https://github.com/d-Rickyy-b/pastepwn/issues/175)
- The DiscordAction now also uses the templating engine - it was forgotten in a previous update ([#176](https://github.com/d-Rickyy-b/pastepwn/issues/176))
- The SyslogAction now also uses the templating engine - it was forgotten in a previous update ([54d3652](https://github.com/d-Rickyy-b/pastepwn/commit/54d3652e4de3fdbaedfdd522f8750aa241890c3c))
- The SaveFileAction does now store each paste in a different file as it should be ([#179](https://github.com/d-Rickyy-b/pastepwn/issues/179))
- The IrcAction did not send the correct data. This was fixed and eventually the action was rewritten from scratch (see "Added")

## [1.2.0] - 2020-02-05
### Added
- Analyzers can now return a boolean or **a list of matched results**
- Actions now get passed a list of matched results by the analyzer
- New Analyzer: PasteTitleAnalyzer - Analyzer to match Paste titles via regex
- New Analyzer: IPv4AddressAnalyzer - Match IPv4 addresses via regex
- Subclasses of RegexAnalyzer now got a method `def verify(results)` that can be overwritten to filter matches so you only return valid results
- EmailPasswordPairAnalyzer has now an optional parameter `min_amount` to specify how many pairs must be found to actually match
- Base64Analyzer got an optional parameter `min_len` to specify how long a detected string must be at least to actually match
- Logical operators for analyzers - you can now connect multiple analyzers with logical operators to specify more precisely when a paste should match ([aed2dbf](https://github.com/d-Rickyy-b/pastepwn/commit/aed2dbf615e7be4586747f5ea6f437663b422f57))
### Changed
- Analyzers can now return a boolean or a list of matched results
- Actions now get passed a list of matched results by the analyzer and can
- IBANAnalyzer will now filter out wrong IBANs and return a list of validated IBANs if the `validate` parameter is set to `True`
### Fixed
- Using non-capturing groups in regex for various analyzers. This is done so that the analyzer can return a matched string and at the same time it fixed some issues with analyzers not matching properly

## [1.1.0] - 2019-11-11
### Added
- Implement TemplatingEngine for filling template strings with content ([8481036](https://github.com/d-Rickyy-b/pastepwn/commit/8481036cc664011bfa5e778a845051426426f134))
- Add custom request headers in request.py ([5043e0c](https://github.com/d-Rickyy-b/pastepwn/commit/5043e0cc05867b92cc058225a331b9e2450cd1e7))
- Add flags to RegexAnalyzer to handle e.g. case insensitive matching ([ddd0dca](https://github.com/d-Rickyy-b/pastepwn/commit/ddd0dcaae707de4c6fe9c1f08fe7d7334e0584f6))
- logger object now usable from within any analyzer ([d21532e](https://github.com/d-Rickyy-b/pastepwn/commit/d21532ef2553ee8a1dca3f41f54b1ab0a0ac37bc))
- Implement logical analyzers (and/or) ([94fc691](https://github.com/d-Rickyy-b/pastepwn/commit/94fc691c0ddba7f201501e74ed0c629e8f219458))
- Implement listify method to create lists from a given input ([e935122](https://github.com/d-Rickyy-b/pastepwn/commit/e935122aa04a729a4abb82a65880e99345b5051f))
- Implement support for onstart handlers ([25b5313](https://github.com/d-Rickyy-b/pastepwn/commit/25b531393eefdec4441ac353e17c42aeb0c2475b))
- Create docker-compose file ([83014be](https://github.com/d-Rickyy-b/pastepwn/commit/83014be091b9f96bc9537d094c49f44cb947489c))
- New Action: TwitterAction for posting tweets when a paste matched ([2056c3c](https://github.com/d-Rickyy-b/pastepwn/commit/2056c3c43a1457e9fd898efc78dc28557efb379f))
- New Action: DiscordAction ([eafdc1c](https://github.com/d-Rickyy-b/pastepwn/commit/eafdc1c2cca851dda202edeed1967bf380460dd3))
- New Action: MISPAction ([8dabe5d](https://github.com/d-Rickyy-b/pastepwn/commit/8dabe5dd126034c0161ce23bb32932a27eb9e5dd))
- New Action: EmailAction ([9cfba96](https://github.com/d-Rickyy-b/pastepwn/commit/9cfba96e6a34595a9deaf18fc494d8f731b01b3b))
- New Action: IrcAction ([fc1d1ab](https://github.com/d-Rickyy-b/pastepwn/commit/fc1d1ab0271e0a62d3da32ea9e344ffacd6be761))
- New Analyzer: PrivateKeyAnalyzer ([a8746f1](https://github.com/d-Rickyy-b/pastepwn/commit/a8746f1a5cd8939b277c8c668dc9def334e9e620))
- New Analyzer: DatabaseDumpAnalyzer ([0aa63ad](https://github.com/d-Rickyy-b/pastepwn/commit/0aa63ada49cf55039bdce0c793df181e661886a5))
- New Analyzer: DBConnAnalyzer ([e940630](https://github.com/d-Rickyy-b/pastepwn/commit/e940630a6347c24afcd4f11f1e302db02b8a5e1c))
- New Analyzer: PhoneNumberAnalyzer ([9ff58b9](https://github.com/d-Rickyy-b/pastepwn/commit/9ff58b9d22b0eaae1b0c9f4d4cabd2dcf94d3ef6))
- New Analyzer: OriginKeyAnalyzer ([d0d715d](https://github.com/d-Rickyy-b/pastepwn/commit/d0d715d9851ebf289717c63b10ccf1759f1df957))
- New Analyzer: SteamKeyAnalyzer ([27273a6](https://github.com/d-Rickyy-b/pastepwn/commit/27273a6f32039641456985c7fe01cf53d5152b75))
- New Analyzer: UplayKeyAnalyzer ([38097ac](https://github.com/d-Rickyy-b/pastepwn/commit/38097ac8225369326455e19a68c0465545fea3d2))
- New Analyzer: EpicKeyAnalyzer ([da122da](https://github.com/d-Rickyy-b/pastepwn/commit/da122dad37395a67003073161ef8b7d6b6cca090))
- New Analyzer: BattleNetKeyAnalyzer ([8927204](https://github.com/d-Rickyy-b/pastepwn/commit/8927204d901ed4275e2995239d2be66fc3e74925))
- New Analyzer: MicrosoftKeyAnalyzer ([8927204](https://github.com/d-Rickyy-b/pastepwn/commit/8927204d901ed4275e2995239d2be66fc3e74925))
- New Analyzer: AWSAccessKeyAnalyzer ([ebc6eab](https://github.com/d-Rickyy-b/pastepwn/commit/ebc6eab54a11fd7ad9dd1959cdc29f314efd9d82))
- New Analyzer: AWSSecretKeyAnalyzer ([d07021a](https://github.com/d-Rickyy-b/pastepwn/commit/d07021a93ac0f64a86393aa3955771643b8e23e5))
- New Analyzer: SlackWebhookAnalyzer ([c40c364](https://github.com/d-Rickyy-b/pastepwn/commit/c40c3647489e8fc6e5e3b0c3e3f9dc5a1d2fd5cb))
- New Analyzer: GoogleOAuthKeyAnalyzer ([fbfb8bf](https://github.com/d-Rickyy-b/pastepwn/commit/fbfb8bf30e1acab0375b3d388cf92e13af696fd5))
- New Analyzer: FacebookAccessTokenAnalyzer ([bb51e3e](https://github.com/d-Rickyy-b/pastepwn/commit/bb51e3e82d954a4a75f478c675e7a7f2c2b9761d))
- New Analyzer: Base64Analyzer ([8d50fbe](https://github.com/d-Rickyy-b/pastepwn/commit/8d50fbe23a31e7e9e4418c4d95dd281c863b9887))
- New Analyzer: AdobeKeyAnalyzer ([4e52345](https://github.com/d-Rickyy-b/pastepwn/commit/4e52345b63ded044ea13744901c728fec7f57aab))
- New Analyzer: EmailPasswordPairAnalyzer ([f0af9cb](https://github.com/d-Rickyy-b/pastepwn/commit/f0af9cbe660c322db7de31676a92186b49f6fa36))
- New Analyzer: HashAnalyzer ([87080c2](https://github.com/d-Rickyy-b/pastepwn/commit/87080c2c3fe1b7ff9f5d200b484061f3b9e6c8e0))
- New Analyzer: SlackTokenAnalyzer ([d686169](https://github.com/d-Rickyy-b/pastepwn/commit/d68616917fd36f33030741a71c0037dc3274d9f4))
- New Analyzer: MailChimpApiKeyAnalyzer ([2e5302d](https://github.com/d-Rickyy-b/pastepwn/commit/2e5302d6faed2acf1e626950b6f0d91fa88e2a09))
- New Analyzer: MegaLinkAnalyzer ([c884cb6](https://github.com/d-Rickyy-b/pastepwn/commit/c884cb60dd17c191aba637dcb8dc4d6675dfc101))
- New Analyzer: StripeApiKeyAnalyzer ([f9bd202](https://github.com/d-Rickyy-b/pastepwn/commit/f9bd202d0813aebb6bc3f189a43158227ca2bdea))
- New Analyzer: AzureSubscriptionKeyAnalyzer ([b010cb5](https://github.com/d-Rickyy-b/pastepwn/commit/b010cb58979c009be943e9f5dd36432e834bda41))
- New Analyzer: GoogleApiKeyAnalyzer ([635a5e4](https://github.com/d-Rickyy-b/pastepwn/commit/635a5e4f1357e458d2d35c7dbd8732d756694ec1))

### Changed
- Add pastebinscraper by default ([d00fc83](https://github.com/d-Rickyy-b/pastepwn/commit/d00fc83dbf094e4fadedb4c5d9b22ad6e8733ace))
- Remove unused custom_payload from DiscordAction ([7b13d75](https://github.com/d-Rickyy-b/pastepwn/commit/7b13d757242af33ddc9ce1c2c3e5e3d7618cd4b5))

### Fixed
- SHA hash analyzer can now accept multiple length hashes ([494d1af](https://github.com/d-Rickyy-b/pastepwn/commit/494d1af5871629bbfd2ee6c859e360e90042ae18))
- Use empty string if paste.body is set to None in URL- and IBANAnalyzer ([09f6763](https://github.com/d-Rickyy-b/pastepwn/commit/09f6763892f22dc6488abfd9d03f73eab232e4ca))
- Include some changes when creating a sqlite file ([0eb3504](https://github.com/d-Rickyy-b/pastepwn/commit/0eb3504e9ad67cea4cd808fd7edb7f4ec862264d))

## [1.0.16] - 2019-09-08
### Added
- Perform checks on pastebin responses to catch errors ([01f865e](https://github.com/d-Rickyy-b/pastepwn/commit/01f865e4acf4f7a92302a28010498732b3514d85))
- If pastes are not ready for downloading, requeue them ([01f865e](https://github.com/d-Rickyy-b/pastepwn/commit/01f865e4acf4f7a92302a28010498732b3514d85))

## [1.0.15] - 2019-09-04
### Added
- Ability to search for multiple words in single WordAnalyzer ([d2a7e09](https://github.com/d-Rickyy-b/pastepwn/commit/d2a7e0957ec1c758be2e76441e50f12b7a08a575))
- Ability to restart running scrapers after adding a new one ([de99892](https://github.com/d-Rickyy-b/pastepwn/commit/de99892f56e0933fee2939bac83c91fad3782994))
- Ability to register error handlers ([1fae47e](https://github.com/d-Rickyy-b/pastepwn/commit/1fae47e0b97f5d42966775d305a6b5561db1dc73))
### Fixed
- Check if paste is None before analyzing it ([2fd7b39](https://github.com/d-Rickyy-b/pastepwn/commit/2fd7b398ab13c3d891b4f0164625ce38f25f205f), [f4bfa46](https://github.com/d-Rickyy-b/pastepwn/commit/f4bfa466c27329839e7155b7f625ef18575ab1a8))
- Broken behaviour for WordAnalyzer blacklist ([df2dd5b](https://github.com/d-Rickyy-b/pastepwn/commit/df2dd5b1627915f1b3996e7c4a10349ad837f7e2))
- Reduced sleep time in order to shut down pastepwn faster ([55bb18d](https://github.com/d-Rickyy-b/pastepwn/commit/55bb18d17ee27e443b244dcd3ea2a0362fc5853a))
- Add check in GenericAnalyzer if parameter is callable ([781d6d0](https://github.com/d-Rickyy-b/pastepwn/commit/781d6d0324fb73d93f9d8789aa08a0e72a597825))
- WordAnalyzer not matching in case sensitive mode ([8762ddd](https://github.com/d-Rickyy-b/pastepwn/commit/8762dddc2a41f01db45549006d8a9707fa1203a6))

## [1.0.14] - 2019-09-04
### Added
- Parameter for setting up storing of all downloaded pastes ([e04f476](https://github.com/d-Rickyy-b/pastepwn/commit/e04f4761ba574df89a4972e7b88281ce57880fb0))
### Fixed
- Broken path to requirements.txt in setup.py ([cc7edf4](https://github.com/d-Rickyy-b/pastepwn/commit/cc7edf41a093b1c53a9b9db309db05a19df3e44d))
- Missing column 'syntax' in sqlite table layout ([3fb3821](https://github.com/d-Rickyy-b/pastepwn/commit/3fb3821115e1973fea4af8835cfac65f48849fed))
- Broken variable substitution for sqlite statement ([cf49963](https://github.com/d-Rickyy-b/pastepwn/commit/cf4996366cf27d7a98bfc06282e241129f771206))
- Allow writing to sqlite db from multiple threads ([f47ec62](https://github.com/d-Rickyy-b/pastepwn/commit/f47ec62cec23fa2adc1f2ed2a8fce04a9b8a041a))

## [1.0.13] - 2019-09-02
### Added
- Pastepwn got a logo! ([57e6665](https://github.com/d-Rickyy-b/pastepwn/commit/57e6665185499b3efef8d023fd83e47c8d4cd7a6))
- Use travis tag when building pypi package ([bda3c7e](https://github.com/d-Rickyy-b/pastepwn/commit/bda3c7ebba9f65ab6e469a653e835013cdf760b2))
### Fixed
- Broken paths in setup.py ([42eca9b](https://github.com/d-Rickyy-b/pastepwn/commit/42eca9bd5a21d01bd2bf1e01c074e9f2748a8948))

## [1.0.12] - 2019-02-20
### Added
- New `add_action(self, action)` method in BasicAnalyzer to add actions on the fly ([4b5df12](https://github.com/d-Rickyy-b/pastepwn/commit/4b5df12450e116a8f6754aeeacf77ba9e8efcd86))
- Created a Dockerfile ([b5334ff](https://github.com/d-Rickyy-b/pastepwn/commit/b5334ff84fae9d4d38fd11ebddfb242cd23cb893))
- Implement possibility to execute multiple actions when a paste matches ([ae6055e](https://github.com/d-Rickyy-b/pastepwn/commit/ae6055e54cb360a97547b97881fdba403e55d0e3))
- Method to create database on a mysql server ([dbfecce](https://github.com/d-Rickyy-b/pastepwn/commit/dbfecceece2f35af99fa68c5bfa67da15fa2db71))
- Stop method for pastedispatcher
- Stop method in actionhandler ()
### Changed
- Minimum supported Python version is now 3.5, because that's what we run travis on ([7b8bae2](https://github.com/d-Rickyy-b/pastepwn/commit/7b8bae246522775fa2c1d1c7664612080ceddd2b))
### Fixed
- Use better sqlite create table statement ([9378dad](https://github.com/d-Rickyy-b/pastepwn/commit/9378dadaf4bd3cbb314a2ecd2429282a72a7dad2))
- MySQL Port setting did not work ([d498088](https://github.com/d-Rickyy-b/pastepwn/commit/d498088b924b76d172c6602879eb9e72743ed238))
- Wrong MySQL syntax in create statements ([6ae6508](https://github.com/d-Rickyy-b/pastepwn/commit/6ae6508bc077c83ac5990839c8548749745fd75e))

## [1.0.11] - 2019-01-09
### Fixed
- Several issues with MySQL adapter ([37c8f36](https://github.com/d-Rickyy-b/pastepwn/commit/37c8f36e8603cb3f68f874a7d85d54a863c1a516))

## [1.0.10] - 2019-01-06
### Added
- Template support for Telegram messages ([3f11cb5](https://github.com/d-Rickyy-b/pastepwn/commit/3f11cb5d5b4f09c9ba3ea49c1b9aa120d9d6a87f))
### Fixed
- Travis config for pypi ([c2608a0](https://github.com/d-Rickyy-b/pastepwn/commit/c2608a0b70e1bb5d4759759a0db77254f02dfebd))
- Wrong MySQL syntax in create statement ([b3afc3d](https://github.com/d-Rickyy-b/pastepwn/commit/b3afc3d0734ad104d29612c404254e79ce28e5c6))

## [1.0.9-travis] - 2018-10-26
### Added
- Travis badge in Readme
- Usage description in Readme

## [1.0.8-travis] - 2018-10-26
### Added
- Travis config file ([dd3db55](https://github.com/d-Rickyy-b/pastepwn/commit/dd3db552a03c40bde3ae2a149d2844a60f886417))

## [1.0.8] - 2018-10-22
First stable release

[unreleased]: https://github.com/d-Rickyy-b/pastepwn/compare/v1.3.1...HEAD
[1.3.1]: https://github.com/d-Rickyy-b/pastepwn/compare/v1.3.0...v1.3.1
[1.3.0]: https://github.com/d-Rickyy-b/pastepwn/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/d-Rickyy-b/pastepwn/compare/v1.1.0...v1.2.0
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
