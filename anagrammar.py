# -*- coding: utf-8 -*-
import typing
from   typing import *

###
# Standard imports.
###

import os
import sys

import argparse
import logging
import math
import multiprocessing
import platform
import pprint
import random
import resource
import string
import time

###
# Parts of this project.
###

from   urdecorators  import trap
from   dictbuilder   import dictbuilder, dictloader
from   sloppytree    import SloppyTree
import urlogger

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

###
# The alphabet order is not relevant to the algorithm. This order
# was chosen to reduce the magnitude of the numbers slightly. In
# one 14 letter phrase, the reduction was from 60 bits to 50 bits.
# keep in mind that all the factors of the large composite numbers
# are small, so the division goes quickly.
###
primes26 = (2, 3, 5, 7, 11, 
    13, 17, 19, 23, 29, 
    31, 37, 41, 43, 47, 
    53, 59, 61, 67, 71, 
    73, 79, 83, 89, 97,
    101 )
primes = dict(zip("eariotnslcudpmhgbfywkvxzjq", primes26))

def word_value(word:str) -> int:
    return math.prod(primes[_] for _ in word)

smallest_word = 1

remainders = set()
tries = 0
deadends = 0
gkey = ""
longest_branch_explored = 0
words={}

"""        0123456789 123456789 123456789 123456789 123456789 """
top_line ="""
 D | branch |  dead  |  user  |  sys   |  page  |  I/O  | WAIT | USEDQ |  Tails  | 
   | evals  |  ends  |  secs  |  secs  | faults |  sig  |  sig |       |         |
---+--------+--------+--------+--------+--------+-------+------+-------+---------|"""
formatter=" {:>2} {: >8} {: >8} {: >8.2f} {: >8.2f} {:> 8} {: >7} {:>6} {:>6} {:>9} keys => {:>6}:{}"

###
# There is no standard way to do this, particularly with virtualization.
###
@trap
def cpucounter() -> int:
    names = {
        'macOS': lambda : os.cpu_count(),
        'Linux': lambda : len(os.sched_getaffinity(0)),
        'Windows' : lambda : os.cpu_count()
        }
    return names[platform.platform().split('-')[0]]()


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


class TimeOut(Exception): pass

time_out = 0

@trap
def find_words(phrase_v:int, 
    factors:tuple, 
    depth:int=0) -> SloppyTree:
    """
    Our formula. This is a recursive function to discover the 
    anagrams. It starts by considering the shortest possible word
    that could be a part of an anagram for the target phrase, and
    progressively considers shorter keys. 

    phrase_v -- the word_value of the string we are finding anagrams for.
        If it is not a large composite number (i.e., strictly greater than 
        any of the factors), then it cannot be part of an anagram, and 
        this is a dead-end. 

    factors -- a tuple of integers that correspond to the potential
        components of the anagram.

    returns -- a SloppyTree of ints representing the integers we
        have evaluated. If the leaf is True, then the path from
        the root to the leaf is an anagram. If the leaf is False,
        then this is a dead-end, and the parent of the leaf
        cannot be a part of an anagram.
    """
    global words, tries, deadends
    logger.info(f"{depth=} , {phrase_v=}")
    global longest_branch_explored
    global smallest_word

    longest_branch_explored = max(depth+1, longest_branch_explored)
    matches = SloppyTree()
    root = matches[phrase_v]

    # Let's start with the largest factor.

    factors = tuple(sorted(prune_dicts(phrase_v, factors)))

    if not factors: 
        root = False
        return
    smallest_factor = factors[0]
    largest_factor = factors[-1]

    try:
        for factor in factors:
            tries += 1
            logger.info(f"{factor=}")
            if not depth and time.time() - start_time > time_out: raise TimeOut('timed out')

            residual, remainder = divmod(phrase_v, factor)
            if remainder:
                logger.warning(f"This is unusual: {phrase_v=} {factor=} {residual=} {remainder=}")
            elif residual in factors: # This is a terminal.
                root[factor] = residual
            elif residual < smallest_factor: # This is a dead-end.
                deadends += 1
            else: # We don't yet know.
                logger.info(f"Recursing. {factor=} {residual=}")
                t = find_words(residual, tuple(_ for _ in factors if _ < residual), depth+1)
                if len(t): root[factor] = t
    except Exception as e:
        logger.error(str(e))
        raise

    finally:
        return root


@trap
def prune_dicts(filter:int, 
    candidates:tuple) -> tuple:
    """
    """
    return {k for k in candidates if not filter % k}


@trap
def anagrammar_main(myargs:argparse.Namespace) -> int:
    """
    Let's build the anagram tree.

    myargs  -- from the command line.

    returns -- an int from os.EX_*
    """
    global tries
    global time_out
    global topline
    global deadends
    global longest_branch_explored
    global smallest_word
    global words

    # If we have been given a limit on CPU, set it.
    time_out = myargs.cpu_time
    if time_out > 0: 
        logger.info(f"This execution is being limited to {myargs.cpu_time} CPU seconds.")
        resource.setrlimit(resource.RLIMIT_CPU, (int(myargs.cpu_time), int(myargs.cpu_time)))

    # Always be nice. Each level of niceness lowers the priority
    # by 10%, so this will roughly cut the CPU proportion to about 1/2
    # of what it was.
    os.nice(7)

    original_words = [ _ for _ in myargs.phrase.lower() if _ in string.ascii_lowercase ]
    original_phrase = "".join(original_words)
    original_phrase_value = word_value(original_phrase)

    min_len  = myargs.min_len
    for i in range(min_len): smallest_word *= primes26[i]

    logger.info(f"{myargs.phrase=}")
    # We cannot work without a dictionary, so let's get it first.
    words= dictloader(myargs.dictionary)
    logger.info(f"Dictionary of {len(words)} words.")

    ###
    # We may not want to use any of the words that were in
    # the original phrase.
    ###
    if myargs.no_dups:
        for w in original_words:
            try:
                del words[word_value(w)]
            except:
                pass

    ###
    # Check for a file of exclusions.
    ###
    if myargs.none_of:
        try:
            with open(myargs.none_of) as words:
                for w in words.read().lower().split():
                    try:
                        del words[word_value(w)]
                    except:
                        pass

        except FileNotFoundError as e:
            logger.debug(f"Unable to open {myargs.none_of}")

    ###
    # The only words we need to consider are the ones that divide
    # the target phrase evenly. This operation greatly reduces
    # the size of the dictionary.
    ###
    words = {k:v for k, v in words.items() if len(v[0]) >= myargs.min_len and 
        original_phrase_value % k == 0}
    smallest_word = min(words) if words else 0
    largest_word = max(words) if words else 0
    logger.info(f"Initial pruning for {original_phrase_value=} {len(words)=}") 
    logger.info(f"{smallest_word=}")
    logger.info(f"{largest_word=}")

    # print(f"{top_line}", file=sys.stderr)

    ###
    # Let's reduce the complexities of dragging around the dictionary, and
    # just leave it here. We'll figure out which words correspond to the 
    # factors when we return.
    ###
    anagrams = SloppyTree()
    try:
        anagrams[original_phrase_value] = find_words(original_phrase_value, tuple(words.keys()))
    except TimeOut:
        pass
    except KeyboardInterrupt as e:
        print("You pressed control C")
    except Exception as e:
        raise
    finally:
        logger.info(f"{anagrams=}")


    numeric_anagrams = set()
    for combo in anagrams.tree_as_table():
        if None not in combo:
            numeric_anagrams.add(tuple(sorted(combo, reverse=True)[1:]))

    for ngram in numeric_anagrams:
        text_gram = tuple(words.get(_) for _ in ngram)
        print(text_gram)

    print(f"{tries=} {deadends=}")

    return sys.exit(os.EX_OK)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog="anagrammar", 
        description="A brute force anagram finder.")

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
    parser.add_argument('-t', '--cpu-time', type=float, default=60,
        help="Set a maximum number of CPU seconds for execution.")
    parser.add_argument('-v', '--verbose', type=int, default=logging.DEBUG,
        help=f"Set the logging level on a scale from {logging.DEBUG} to {logging.CRITICAL}.")
    parser.add_argument('-z', '--zap', action='store_true', 
        help="If set, remove old logfile.")

    parser.add_argument('phrase', type=str,
        help="The phrase. If it contains spaces, it must be in quotes.")

    myargs = parser.parse_args()
    if myargs.nice: os.nice(myargs.nice)
    if myargs.zap:
        try:
            os.unlink('anagrammar.log')
        except:
            pass
    logger = urlogger.URLogger(logfile='anagrammar.log', level=myargs.verbose)    
    logger.info(dump_cmdline(myargs))

    sys.exit(anagrammar_main(myargs))
