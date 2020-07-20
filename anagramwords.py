#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import typing
from   typing import *

import os
import sys

from   collections import Counter
import copy
import functools
from   functools import total_ordering
import math
import os.path
import platform
import time

from   gkfdecorators import show_exceptions_and_frames as trap

# Credits
__author__ = 'George Flanagin'
__copyright__ = 'Copyright 2020'
__credits__ = None
__version__ = str(1/math.pi)
__maintainer__ = 'George Flanagin'
__email__ = ['me@georgeflanagin.com', 'gflanagin@richmond.edu']
__status__ = 'Teaching example'
__license__ = 'MIT'

class CountedWord: pass

@total_ordering
class CountedWord(Counter):
    """
    Each word/phrase corresponds to one CountedWord representation of it.
    For example, CountedWord('georgeflanagin') is 'aaeefgggilnnor'. However, 
    the same CountedWord may be a representation of many different words.

    The operators allow us to write code that is somewhat algebraic.
    """
    def __init__(self, s:str):
        """
        Add one class member, the as_str, which is a the word
        represented as a 
        """
        Counter.__init__(self, s)
        self.as_str = "".join(sorted(self.elements()))


    def __eq__(self, other:Union[CountedWord,str]) -> bool:
        """ 
        if CountedWord(w1) == CountedWord(w2), then w1 and w2 are
        anagrams of each other.  For example CountedWord('loaf') ==
        CountedWord('foal').
        """
        if isinstance(other, str): other = CountedWord(other)
        return self.as_str == other.as_str


    def __le__(self, other:Union[CountedWord,str]) -> bool:
        """
        if shred1 <= shred2, then shred1 is in shred2
        """
        if isinstance(other, str): other=Counter(other)
        
        # Note that there are no zero-counts in the Counter's 
        # dict. So all the v-s from self will be > 0.
        return all(other.get(c, 0) >= v for c, v in self.items())  


    def __sub__(self, other:CountedWord) -> CountedWord:
        if isinstance(other, (str, Counter)): other = CountedWord(other)
        if other <= self:
            x = copy.copy(self)
            x.subtract(other)
            x.__clean()
            x.as_str = "".join(sorted(x.elements()))
            return x
        else:
            raise ValueError('RHS is not <= LHS') 


    def __add__(self, other:CountedWord) -> CountedWord:
        if isinstance(other, (str, Counter)): other = CountedWord(other)
        x = copy.copy(self)
        x.update(other)
        x.as_str = "".join(sorted(self.elements()))
        return x


    def __clean(self) -> None:
        zeros = [ k for k in self if self[k] == 0 ]
        for k in zeros:
            self.pop(k)


    def __str__(self) -> str:
        """
        The contents, sorted, and as a string.
        """
        return self.as_str

