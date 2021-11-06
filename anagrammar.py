# -*- coding: utf-8 -*-
import typing
from   typing import *

###
# Standard imports.
###

import os
import sys

import argparse
import math
import multiprocessing
import platform
import random
import resource
import string
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

###########################################################################
# Global variables that make things easier for programming the reporting
# part of the tool.
# 
# current_key -- current key being examined at the root of the tree.
# deadends -- the number of branches that have no anagrams.
# exhausted_keys -- set containing the keys that have been checked.
# longest_branch_explored -- "max depth" of the tree.
# num_exhausted -- the size of exhausted_keys.
# order -- set to 0, 1, or 2 for random, shortest first, longest first.
# remainders -- 
# tries -- how many tries.
# vvv -- global boolean for verbosity.
############################################################################
current_key = ""
deadends = 0
exhausted_keys = set()
longest_branch_explored = 0
num_exhausted = 0
order = -1
remainders = set()
tries = 0
vvv = False

############################################################################
# Decoration for our live updates during execution.
############################################################################
"""        0123456789 123456789 123456789 123456789 123456789 """
top_line ="""
 D | branch |  dead  |  user  |  sys   |  page  |  I/O  | WAIT | USEDQ | Key Num | 
   | evals  |  ends  |  secs  |  secs  | faults |  sig  |  sig |       |         |
---+--------+--------+--------+--------+--------+-------+------+-------+---------|"""
formatter=" {:>2} {: >8} {: >8} {: >8.2f} {: >8.2f} {:> 8} {: >7} {:>6} {:>6} {:>9}"

@trap
def cpucounter() -> int:
    # There is no standard way to do this, particularly with virtualization.
    names = {
        'macOS': lambda : os.cpu_count(),
        'Linux': lambda : len(os.sched_getaffinity(0)),
        'Windows' : lambda : os.cpu_count()
        }
    return names[platform.platform().split('-')[0]]()


def debug(s:str) -> bool:
    global vvv
    if vvv > 3: sys.stderr.write(f"{s}\n")
    return vvv > 2


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
    depth -- keep track of the recursion level

    returns -- a SloppyTree whose keys are the qualifying keys from
        the reverse_dict. The values are either a SloppyTree containing
        keys, or None, never an empty SloppyTree.
    """

    global current_key
    global deadends
    global exhausted_keys
    global longest_branch_explored
    global num_exhausted
    global order
    global remainders
    global tries

    # For us to consider the parts, the phrase must be long enough to
    # be broken into parts.
    if len(phrase) < min_len * 2: 
        deadends += 1
        debug(f"{phrase.as_str} too short.")
        return None

    longest_branch_explored = max(depth+1, longest_branch_explored)
    matches = SloppyTree()

    f_dict, r_dict = prune_dicts(phrase, forward_dict, reversed_dict, min_len)
    if isinstance(phrase, str): phrase = CountedWord(phrase)

    # Create an iterator for the keys based on the preferred order.
    keys_by_size = (
        (_ for _ in sorted(r_dict.keys(), key=len, reverse=(order==2))) 
        if order else
        (_ for _ in random.sample(r_dict.keys(), len(r_dict)))
        )


    ##################################################################33
    # Let's iterate
    ##################################################################33
    for i, key in enumerate(keys_by_size):
        tries += 1
        if depth==1: current_key = key
        if key in exhausted_keys: continue
        if not vvv and not tries%100: stats(depth) 

        # "key" maps to at least one word, and "remainder" is the
        # part about which we are uncertain.
        remainder = phrase - key
        debug(f"{key=} remainder={remainder.as_str}")

        if len(remainder.as_str) < min_len:
            debug(f"len({remainder.as_str}) < {min_len}")
            continue
        
        if str(remainder) in exhausted_keys: 
            debug(f"{remainder.as_str} is exhausted.")
            continue

        # Is there at least one word that can be made from the
        # complete remainder string?
        if str(remainder) in r_dict:
            debug(f"{remainder.as_str} in r_dict")
            matches[key] = remainder
            continue

        else:
            if len(remainder) < min_len*2:
                debug(f"{remainder.as_str} too short to recurse.")
                continue
            else:
                debug(f"{remainder.as_str} recursing to level {depth+1}")
                matches[key] = find_words(
                    remainder, f_dict, r_dict, min_len, depth=depth+1)

        if not matches[key]: 
            deadends += 1
            del matches[key]

        # At this point, we have thoroghly examined remainder, and there is no
        # reason to look at it again.
        debug(f"{remainder.as_str} is a new dead end.")
        if depth==1:
            exhausted_keys.add(key)
            num_exhausted += 1

    return matches if len(dict(matches)) else None


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
        if isinstance(replacements[str(t)], tuple):
            return ( replacements[str(t)][0] 
                if len(replacements) == 1 else
                replacements[str(t)] )

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
    global deadends
    global current_key
    global num_exhausted

    info = resource.getrusage(resource.RUSAGE_SELF)
    print(formatter.format(
        depth+1,
        tries,
        deadends,
        info[0],    # user mode time in seconds.
        info[1],    # system mode time in seconds.
        info[6],    # page faults not requiring I/O
        info[7],    # page faults that do require I/O
        info[14],   # giving up time
        info[15],   # USEDQ, pre-emptive reschedule.
        num_exhausted
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
    if myargs.cpu_time > 0: 
        print(f"This execution is being limited to {myargs.cpu_time} CPU seconds.")
        resource.setrlimit(resource.RLIMIT_CPU, (int(myargs.cpu_time), int(myargs.cpu_time)))

    # Always be nice. Each level of niceness lowers the priority
    # by 10%, so this will roughly cut the CPU proportion to about 1/2
    # of what it was.
    os.nice(7)

    original_words = [ _ for _ in myargs.phrase.lower() 
        if _ in string.ascii_lowercase ]
    original_phrase = "".join(original_words)
    original_phrase_XF = CountedWord(original_phrase)

    min_len  = myargs.min_len

    # We cannot work without a dictionary, so let's get it first.
    print(myargs.phrase)
    words, XF_words = dictloader(myargs.dictionary)
    print(f"{len(words)=} {len(XF_words)}")

    ###
    # We may not want to use any of the words that were in
    # the original phrase.
    ###
    exclusions = []
    if myargs.no_dups:
        for w in original_words:
            k = words.get(w)     # Get the corresponding XF_word
            if k is not None: exclusions.append(k)

    ###
    # Check for a file of exclusions.
    ###
    if myargs.none_of:
        try:
            with open(myargs.none_of) as words:
                exclusions.extend(words.read().lower().split())
        except FileNotFoundError as e:
            print(f"Unable to open {myargs.none_of}")

    ###
    # Remove all of the words we have collected.
    ###
    for w in exclusions: 
        k = words.get(w)
        if k is None: continue

        t = XF_words[k]
        t = tuple(_ for _ in t if _ != w)
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
    anagrams = find_words(original_phrase, words, XF_words, myargs.min_len)
    anagrams = replace_XF_keys(anagrams, XF_words)
    self_anagrams = XF_words.get(CountedWord(original_phrase).as_str, None)
    if self_anagrams is not None and len(self_anagrams) > 1:
        self_anagrams = tuple([_ for _ in self_anagrams if not _ == original_phrase])
        anagrams[original_phrase] = self_anagrams
    stats(0)
    print(f"\n\n{tries} branches in the tree. {deadends} dead ends. Max depth {longest_branch_explored+1}.", 
        file=sys.stderr)
    print(f"{anagrams}")
    print(f"{len(anagrams)} anagrams for {myargs.phrase} were found.")

    return sys.exit(os.EX_OK)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="anagrammar", 
        description="A brute force anagram finder.")

    parser.add_argument('-t', '--cpu-time', type=float, default=0,
        help="Set a maximum number of CPU seconds for execution.")
    parser.add_argument('-x', '--cores', type=int, default=1, 
        choices=range(1, cpucounter()),
        help="Number of cores on which to execute.")
    parser.add_argument('-d', '--dictionary', type=str, required=True,
        help="Name of the dictionary of words, or a pickle of the dictionary.")
    parser.add_argument('-m', '--min-len', type=int, default=2,
        help="Minimum length of any word in the anagram")
    parser.add_argument('--nice', type=int, choices=range(0, 20), default=0,
        help="Niceness may affect execution time.")
    parser.add_argument('--no-dups', action='store_true',
        help="Disallow words that were in the original phrase.")
    parser.add_argument('--none-of', type=str, default=None,
        help="Exclude all words in the given filename.")
    parser.add_argument('-o', '--order', type=int, choices=(0, 1, 2), default=1,
        help="Key ordering: 0: random, 1:shortest first, 2:longest first")
    parser.add_argument('-v', '--verbose', type=int, default=0, choices=(0, 1, 2, 3),
        help="Be chatty about what is taking place -- on a scale of 0 to 3")

    parser.add_argument('phrase', type=str,
        help="The phrase. If it contains spaces, it must be in quotes.")

    myargs = parser.parse_args()
    if myargs.nice: os.nice(myargs.nice)
    dump_cmdline(myargs)
    order = myargs.order

    sys.exit(anagrammar_main(myargs))
