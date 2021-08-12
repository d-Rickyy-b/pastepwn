# -*- coding: utf-8 -*-
import hashlib
import re
from .regexanalyzer import RegexAnalyzer


class HashAnalyzer(RegexAnalyzer):
    """Analyzer to match multiple hashes of user-given passwords."""
    name = "HashAnalyzer"

    def __init__(self, actions, passwords, algorithms=None):
        """Hashes given passwords with multiple algorithms and matches the output.

        :param actions: A single action or a list of actions to be executed on every paste
        :param passwords: A single password or a list of passwords to hash, as bytes
        :param algorithms: A list of algorithm names to use for hashing. This should be a subset
                           of hashlib.algorithms_available, and defaults to it.
        """
        # Make sure passwords is a list
        if isinstance(passwords, bytes):
            passwords = [passwords]

        # Build algorithm list
        if algorithms is None:
            algorithms = hashlib.algorithms_available
        else:
            algorithms = set(algorithms).intersection(hashlib.algorithms_available)

        if not algorithms:
            raise ValueError("No valid algorithm names specified")

        # Compute hashes with all algorithms
        hashes = []
        for hash_name in algorithms:
            hash_function = hashlib.new(hash_name)
            for password in passwords:
                hash_ = hash_function.copy()
                hash_.update(password)
                if hash_name == "shake_128":
                    digest = hash_.hexdigest(128)
                elif hash_name == "shake_256":
                    digest = hash_.hexdigest(256)
                else:
                    digest = hash_.hexdigest()
                hashes.append(digest)

        # Build regex
        regex = r"\b(%s)\b" % "|".join(hashes)
        super().__init__(actions, regex, re.IGNORECASE)
