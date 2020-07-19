# -*- coding: utf-8 -*-
import typing
from   typing import *

import os
import sys

import argparse
from   functools import total_ordering
import math
import platform
import resource
import time

from   gkfdecorators import show_exceptions_and_frames as trap
import anagramwords
from   anagramwords import CountedWord
from   dictbuilder import dictbuilder, dictloader
from   sloppytree import SloppyTree

###
# Credits
###
__author__ = 'George Flanagin'
__copyright__ = 'Copyright 2020'
__credits__ = None
__version__ = str(1/math.pi)
__maintainer__ = 'George Flanagin'
__email__ = ['me@georgeflanagin.com', 'gflanagin@richmond.edu']
__status__ = 'Teaching example'

this_os = platform.system()
if this_os == 'Linux':
    default_word_list = '/usr/share/dict/linux.words'
elif this_os == 'Darwin':
    default_word_list = '/usr/share/dict/words'
else:
    default_word_list = './words'


###
# Just for curiosity, I wonder how long these things take.
###
start_time = time.time()
def time_print(s:str) -> None:
    print("{} : {}".format(round(time.time()-start_time, 3), s))

limit = sys.maxsize
vvv = False
seen = set()


@trap
def find_words(phrase:str, 
    forward_dict:dict, 
    reversed_dict:dict, 
    min_len:int=0) -> SloppyTree:
    """
    Our formula. This is a recursive function to discover the 
    anagrams. 

    phrase -- the string for which we are trying to find anagrams.
    forward_dict -- keys are dictionary words, and values are the same
        letters, sorted.
    reverse_dict -- keys are collections of sorted letters, and the values
        are the dictionary words that can be spelt using them.
    min_len -- the boundary.

    returns -- a SloppyTree whose keys are the qualifying keys from
        the reverse_dict. The values are either a SloppyTree containing
        keys, or None.
    """

    global vvv
    global seen

    if len(phrase) < min_len * 2: 
        return None

    matches = SloppyTree()

    f_dict, r_dict = prune_dicts(phrase, forward_dict, reversed_dict, min_len)
    if isinstance(phrase, str): phrase = CountedWord(phrase)
    keys_by_size = [ _ for _ in sorted(r_dict.keys(), key=len, reverse=True) if _ not in seen ]

    for i, k in enumerate(keys_by_size):
        remainder = phrase - k
        
        if str(remainder) in r_dict:
            matches[k] = remainder.as_str if len(k) >= len(remainder.as_str) else None
            seen.add(remainder.as_str)
        else:
            matches[k] = find_words(remainder, f_dict, r_dict, min_len)

        if matches[k] is None: del matches[k]

    return matches if len(matches) else None


@trap
def prune_dicts(filter:str, 
    forward_dict:dict, 
    reversed_dict:dict, 
    minlen:int=0) -> tuple:
    """
    Apply the filter to the dictionaries, and return a tuple of
        filtered (smaller) dictionaries.
    """
    filter_XF = CountedWord(filter)

    ###
    # The reversed dict gets all the key/word combos that could 
    # be part of anagrams of the filter.
    ###
    filtered_reversed_dict = { k : v for 
        k, v in reversed_dict.items() 
        if len(k) > minlen and CountedWord(k) <= filter_XF }

    ###
    # With the forward filtering, we start with the contents
    # of the reversed dict, pull out the words from the tuples,
    # make them the keys, and use the common key as the value for
    # each word.
    ###
    filtered_forward_dict = {}
    for word_tuple in filtered_reversed_dict.values():
        for word in word_tuple:
            filtered_forward_dict[word] = forward_dict[word]

    # print(f"forward {filtered_forward_dict}")
    # print(f"reversed {filtered_reversed_dict}")
        
    return filtered_forward_dict, filtered_reversed_dict


@trap
def replace_XF_keys(t:SloppyTree, replacements:dict) -> SloppyTree:
    """
    Replace the sorted strings that we have been using in the anagrammar with
    the tuples of words that can be formed from the sorted string. Tuples
    are hashable, so they can be used as keys
    """
    new_tree = SloppyTree()

    if not isinstance(t, SloppyTree): return replacements[t]    

    for k in t:
        new_tree[replacements[k]] = replace_XF_keys(t[k], replacements)

    return new_tree


@trap
def anagrammar_main(myargs:argparse.Namespace) -> int:
    """
    Let's build the anagram tree.

    myargs  -- from the command line.

    returns -- an int from os.EX_*
    """

    resource.setrlimit(resource.RLIMIT_CPU, (myargs.cpu, myargs.cpu))

    original_phrase = "".join(myargs.phrase.lower().split())
    original_phrase_XF = CountedWord(original_phrase)
    vvv = myargs.verbose
    min_len  = myargs.min_len

    # We cannot work without a dictionary, so let's get it first.
    words, XF_words = dictloader(myargs.dictionary)

    ###
    # We will make an initial pruning of the dictionaries, and then
    # delete the plenum dictionaries by letting them go out of scope.
    ###
    words, XF_words = prune_dicts(original_phrase, words, XF_words, myargs.min_len)
    print(f"Initial pruning gives {len(words)} forward and {len(XF_words)} reversed terms.")

    anagrams = find_words(original_phrase, words, XF_words, min_len)
    anagrams = replace_XF_keys(anagrams, XF_words)
    print(f"{anagrams}")

    return sys.exit(os.EX_OK)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog="anagrammar", 
        description="A brute force anagram finder.")
    parser.add_argument('-v', '--verbose', action='store_true',
        help="Be chatty about what is taking place.")
    parser.add_argument('--cpu', type=float, default=5.0,
        help="Set a maximum number of CPU seconds for execution.")
    parser.add_argument('--min-len', type=int, default=3,
        help="Minimum length of any word in the anagram")
    parser.add_argument('--max-depth', type=int, default=4, 
        help="Maximum number of words in the anagram.")
    parser.add_argument('phrase', type=str, 
        help="The phrase. If it contains spaces, it must be in quotes.")
    parser.add_argument('--dictionary', type=str, required=True,
        help="Name of the dictionary of words, or a pickle of the dictionary.")

    myargs = parser.parse_args()
    if myargs.verbose: myargs.limit = 100

    sys.exit(anagrammar_main(myargs))
