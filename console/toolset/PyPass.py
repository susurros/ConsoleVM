#!/usr/bin/env python
#
# PyPass - Python Random Password Generator
#
# Author - Honza Pokorny <me@honza.ca>
# (c) 2010 - Licensed under GPLv3
#https://github.com/honza/pypass/blob/master/pypass.py

import random
import string
import sys


class PyPass(object):
    """
    PyPass Strong Password Generator
    It makes sure no character is repeated. By default, it includes uppercase,
    lowercase, numbers, and punctuation. Lowercase and uppercase are treated as
    separate types (you could have K and k in one password).
    """

    LOWER = string.ascii_lowercase
    UPPER = string.ascii_uppercase
    SPECIAL = string.punctuation

    def __init__(self, length=20):
        self.length = length
        self.last = 1
        self._upper = []
        self._lower = []
        self._numbers = []

    def _get_lower(self):
        a = self.LOWER[random.randint(1, len(self.LOWER) - 1)]
        while True:
            a = self.LOWER[random.randint(1, len(self.LOWER) - 1)]
            if a not in self._lower:
                break
        self._lower.append(a)
        self.last = 1
        return a

    def _get_upper(self):
        a = self.UPPER[random.randint(1, len(self.UPPER) - 1)]
        while True:
            a = self.UPPER[random.randint(1, len(self.UPPER) - 1)]
            if a not in self._upper:
                break
        self._upper.append(a)
        self.last = 2
        return a

    def _get_number(self):
        a = random.randint(1, 10)
        while True:
            a = random.randint(1, 10)
            if a not in self._numbers:
                break
        self._numbers.append(a)
        self.last = 3
        return str(a)


    def _get_next(self):
        i = 0
        while True:
            i = random.randint(1, 3)
            if i != self.last:
                break
        if i == 1:
            return self._get_lower()
        elif i == 2:
            return self._get_upper()
        elif i == 3:
            return self._get_number()
        else:
            pass

    def _reset(self):
        """
        Reset lists of used characters. Used when generating multiple passwords
        """
        self._special = []
        self._lower = []
        self._upper = []
        self._numbers = []

    def run(self):
        self._reset()
        s = ""
        self.last = ""
        for a in range(0, self.length):
            s += self._get_next()
        return s


