# Analyzers
This directory contains all the analyzers for pastepwn. An analyzer is a class that extends the [BasicAnalyzer]() class (or any other subclass of that) and overrides at least the `match` function.

The match function gets passed a paste object. 
The job of an analyzer is to check if a paste matches certain criteria. If it matches, pastepwn will execute the action(s), that is stored in the analyzer.


## Example analyzers
Analyzers can check for multiple things.
A paste contains a certain, previously defined string.
Or the paste matches a certain regex.
Or the paste's syntax is set to `java`.
And many other things.

Check a few selected examples to get an idea:
- [RegexAnalyzer](https://github.com/d-Rickyy-b/pastepwn/blob/master/pastepwn/analyzers/regexanalyzer.py) - Foundation for most other analyzers. Checks a
 paste against a regex
- [SteamKeyAnalyzer](https://github.com/d-Rickyy-b/pastepwn/blob/master/pastepwn/analyzers/steamkeyanalyzer.py) - Checks if a paste contains a Steam Key
- [IBANAnalyzer](https://github.com/d-Rickyy-b/pastepwn/blob/master/pastepwn/analyzers/ibananalyzer.py) - Checks if a paste contains an IBAN


## Create own analyzer
Check out the implementations of a few analyzers and you'll get an idea on how to get started.

```
# -*- coding: utf-8 -*-
from .basicanalyzer import BasicAnalyzer


class MyAnalyzer(BasicAnalyzer):
    name = "MyAnalyzer"

    def __init__(self, actions, regex, flags=0, blacklist=None):
        # We need co call the init of super, to initialize some settings in the basicanalyzer
        super().__init__(actions, self.name)
        
        # We can do some custom setup stuff to initialize e.g. blacklists
        self.blacklist = blacklist or []

    def match(self, paste):
        # Here our pastes get matched. We can access all fields of the paste object
        paste_title = paste.title or ""
        return self.regex.findall(paste_title)
```
 
## Combining analyzers
To combine multiple analyzers and hence multiple conditions, you can use bitwise operators.
Those bitwise operators act as a logical operators by creating a new `MergedAnalyzer` class that handles the individual analyzers internally. 

`&` - bitwise AND for combining analyzers with a logical AND  
`|` - bitwise OR for combining analyzers with a logical OR

```
analyzer1 = SomeAnalyzer(...)
analyzer2 = SomeOtherAnalyzer(...)
analyzer3 = ThirdAnalyzer(...)

realAnalyzer = (analyzer1 & analyzer2) | analyzer3
```

The `realAnalyzer` only matches if either `analyzer1` and `analyzer2` both match, or if `analyzer3` matches.

