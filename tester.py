import os
import sys

vvv = True

from anagramwords import CountedWord
from dictbuilder import dictloader
f_dict, r_dict = dictloader('words')

from anagrammar import prune_dicts, find_words

Phrase = CountedWord('georgeflanagin')
Long = CountedWord('long')
Fearing = CountedWord('fearing')
Age = CountedWord('age')


