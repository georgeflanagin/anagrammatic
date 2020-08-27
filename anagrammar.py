# -*- coding: utf-8 -*-
import typing
from   typing import *

###
# Standard imports.
###

import os
import sys

import argparse
from   functools import total_ordering
import math
import platform
import resource
import time

###
# Parts of this project.
###

from   gkfdecorators import show_exceptions_and_frames as trap
import anagramwords
from   anagramwords  import CountedWord
from   dictbuilder   import dictbuilder, dictloader
from   sloppytree    import SloppyTree

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
__license__ = 'MIT'

###
# Just for curiosity, I wonder how long these things take.
###
start_time = time.time()
def time_print(s:str) -> None:
    print("{} : {}".format(round(time.time()-start_time, 3), s))

# So we don't waste our time examining things twice.
seen = set()
vvv = False
tries = 0
deadends = 0
longest_branch_explored = 0

"""        0123456789 123456789 123456789 123456789 123456789 """
top_line ="""
 #|branch | seen | user |  sys |  page  |  I/O  | WAIT | USEDQ | 
  | evals | keys |  sec | faults | faults|  sig |  sig |       |"""
formatter="{:>2} {: >7} {: >6} {: >6.2f} {: >6.2f} {:> 7} {: >7} {:>6} {:>6}"

@trap
def dump_cmdline(args:argparse.ArgumentParser, return_it:bool=False) -> str:
    """
    Print the command line arguments as they would have been if the user
    had specified every possible one (including optionals and defaults).
    """

    if not return_it: print("")
    opt_string = ""
    for _ in sorted(vars(args).items()):
        opt_string += " --"+ _[0].replace("_","-") + " " + str(_[1])
    if not return_it: print(opt_string + "\n", file=sys.stderr)

    return opt_string if return_it else ""


@trap
def find_words(phrase:str, 
    forward_dict:dict, 
    reversed_dict:dict, 
    min_len:int=0,
    depth:int=0) -> SloppyTree:
    """
    Our formula. This is a recursive function to discover the 
    anagrams. It starts by considering the longest possible word
    that could be a part of an anagram for the target phrase, and
    progressively considers shorter keys. 

    phrase -- the string for which we are trying to find anagrams.
    forward_dict -- keys are dictionary words, and values are the same
        letters, sorted.
    reverse_dict -- keys are collections of sorted letters, and the values
        are the dictionary words that can be spelt using them.
    min_len -- the boundary.

    returns -- a SloppyTree whose keys are the qualifying keys from
        the reverse_dict. The values are either a SloppyTree containing
        keys, or None, never an empty SloppyTree.
    """

    global seen
    global vvv
    global tries
    global deadends
    global longest_branch_explored

    # For us to consider the parts, the phrase must be long enough to
    # be broken into parts.
    if len(phrase) < min_len * 2: 
        deadends += 1
        return None

    longest_branch_explored = max(depth+1, longest_branch_explored)
    matches = SloppyTree()

    f_dict, r_dict = prune_dicts(phrase, forward_dict, reversed_dict, min_len)
    if isinstance(phrase, str): phrase = CountedWord(phrase)
    keys_by_size = [ _ for _ in sorted(r_dict.keys(), key=len, reverse=True) if _ not in seen ]

    for i, k in enumerate(keys_by_size):
        tries += 1
        if not tries%100: stats(depth) 
        remainder = phrase - k
        
        if str(remainder) in r_dict:
            if len(k) >= len(remainder):
                matches[k] = remainder.as_str
                if depth == 0: seen.add(k) 
            if remainder.as_str in matches: 
                matches[k] = None
        else:
            matches[k] = find_words(remainder, f_dict, r_dict, min_len, depth=depth+1)

        if matches[k] is None: 
            deadends += 1
            del matches[k]

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
        if len(k) >= minlen and CountedWord(k) <= filter_XF }

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
    if t is None: return new_tree

    # Find out if we are at a leaf.
    if not isinstance(t, SloppyTree): 
        if isinstance(replacements[t], tuple) and len(replacements[t]) == 1:
            return replacements[t][0]

        return replacements[t]    

    for k in t:
        result = replace_XF_keys(t[k], replacements)
        new_key = replacements[k] if len(replacements[k]) > 1 else replacements[k][0]
        new_tree[new_key] = result
        # new_tree[replacements[k]] = replace_XF_keys(t[k], replacements)

    return new_tree


@trap
def stats(depth:int) -> None:
    """
    Print a line of statistics.
    """
    global tries
    global formatter

    info = resource.getrusage(resource.RUSAGE_SELF)
    print(formatter.format(
        depth+1,
        tries,
        len(seen),  # keys looked at so far.
        info[0],    # user mode time in seconds.
        info[1],    # system mode time in seconds.
        info[6],    # page faults not requiring I/O
        info[7],    # page faults that do require I/O
        info[14],   # giving up time
        info[15]    # USEDQ, pre-emptive reschedule.
        ),  end="\r", file=sys.stderr)
    

@trap
def anagrammar_main(myargs:argparse.Namespace) -> int:
    """
    Let's build the anagram tree.

    myargs  -- from the command line.

    returns -- an int from os.EX_*
    """
    global vvv
    global tries
    global topline
    global deadends
    global longest_branch_explored

    vvv = myargs.verbose

    # If we have been given a limit on CPU, set it.
    if myargs.cpu > 0: 
        print(f"This execution is being limited to {myargs.cpu} CPU seconds.")
        resource.setrlimit(resource.RLIMIT_CPU, (myargs.cpu, myargs.cpu))

    # Always be nice. Each level of niceness lowers the priority
    # by 10%, so this will roughly cut the CPU proportion to about 1/2
    # of what it was.
    os.nice(7)

    original_words = myargs.phrase.lower().split()
    original_phrase = "".join(original_words)
    original_phrase_XF = CountedWord(original_phrase)

    min_len  = myargs.min_len

    # We cannot work without a dictionary, so let's get it first.
    print("Loading dictionaries.")
    words, XF_words = dictloader(myargs.dictionary)
    print("Dictionaries loaded.") 

    # We probably do not want to use any of the words that were in
    # the original phrase.
    if myargs.no_dups:
        for w in original_words:
            k = words.get(w)     # Get the corresponding XF_word
            if k is None: continue

            t = XF_words[k]  # Get the tuple.
            t = tuple(_ for _ in t if _ != w) # Build a new tuple.
            if len(t):
                XF_words[k] = t
            else:
                XF_words.pop(k)

    ###
    # We will make an initial pruning of the dictionaries, and then
    # delete the plenum dictionaries by letting them go out of scope.
    ###
    words, XF_words = prune_dicts(original_phrase, words, XF_words, myargs.min_len)
    print(f"Initial pruning: {len(XF_words)} keys representing {len(words)} words.", 
        file=sys.stderr)

    print(f"{top_line}", file=sys.stderr)
    print(65*'-', file=sys.stderr)
    anagrams = find_words(original_phrase, words, XF_words, myargs.min_len)
    anagrams = replace_XF_keys(anagrams, XF_words)
    stats(0)
    print(f"\n\n{tries} branches in the tree. {deadends} dead ends. Max depth {longest_branch_explored+1}.", 
        file=sys.stderr)
    print(f"{anagrams}")

    return sys.exit(os.EX_OK)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog="anagrammar", 
        description="A brute force anagram finder.")

    parser.add_argument('-v', '--verbose', action='store_true',
        help="Be chatty about what is taking place.")
    parser.add_argument('--cpu', type=float, default=0,
        help="Set a maximum number of CPU seconds for execution.")
    parser.add_argument('--min-len', type=int, default=2,
        help="Minimum length of any word in the anagram")
    parser.add_argument('--no-dups', action='store_true',
        help="Disallow words that were in the original phrase.")
    parser.add_argument('phrase', type=str, 
        help="The phrase. If it contains spaces, it must be in quotes.")
    parser.add_argument('--dictionary', type=str, required=True,
        help="Name of the dictionary of words, or a pickle of the dictionary.")

    myargs = parser.parse_args()
    dump_cmdline(myargs)

    sys.exit(anagrammar_main(myargs))
