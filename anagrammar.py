# -*- coding: utf-8 -*-
import typing
from   typing import *

###
# Standard imports.
###

import os
import sys

import argparse
import itertools
import logging
import math
import multiprocessing
import string
import time

###
# Parts of this project.
###

from   urdecorators  import trap
from   dictbuilder   import dictloader
from   sloppytree    import SloppyTree
import urlogger

###
# Credits
###
__author__ = 'George Flanagin'
__copyright__ = 'Copyright 2023'
__credits__ = None
__version__ = str(1/math.pi)
__maintainer__ = 'George Flanagin'
__email__ = ['me@georgeflanagin.com', 'gflanagin@richmond.edu']
__status__ = 'Teaching example'
__license__ = 'MIT'

###
# Globals.
###
logger = None

###
# Just for curiosity, I wonder how long these things take.
###
start_time = time.time()

###
# These globals contain the mapping of prime numbers to letters
# in the alphabet, and the mapping of composite numbers to
# a tuple of words from the dictionary that map to the composite
# number.
###
prime_map = {}
words={}

@trap
def word_value(word:str) -> int:
    return math.prod(prime_map[_] for _ in word)

# Continuously updated to reflect the value of the root
# of the current branch of the tree we are evaluating.
current_root = 1

# A collection of previously evaluated roots.
seen_roots = set()

# The word of least value in the dictionary.
smallest_word = 1

# See if we have run long enough to quit.
time_out = 0

# Dead ends are words (numbers) that cannot be a part
# of this anagram.
dead_ends = set()

stats = SloppyTree()
stats.tries = 0       # number of edges considered.
stats.nodes = 0       # number of level 0 edges.
stats.factors = 0
stats.dead_ends = 0

@trap
def dump_cmdline(args:argparse.ArgumentParser, return_it:bool=False) -> str:
    """
    Print the command line arguments as they would have been if the user
    had specified every possible one (including optionals and defaults).
    """
    opt_string = ""
    for _ in sorted(vars(args).items()):
        opt_string += " --"+ _[0].replace("_","-") + " " + str(_[1])
    if not return_it: print(opt_string + "\n", file=sys.stderr)

    return opt_string if return_it else ""


@trap
def find_words(phrase_v:int,
    factors:tuple,
    depth:int=0) -> SloppyTree:
    """
    This is a recursive function to discover the anagrams. It starts by
    considering the shortest possible word that could be a part of an
    anagram for the target phrase, and progressively applies the same
    logic to shorter residuals.

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
    logger.debug(f"{depth=} , {phrase_v=}")
    global current_root
    global dead_ends
    global seen_roots
    global smallest_word
    global stats

    # This will be our return value.
    matches = SloppyTree()
    root = matches[phrase_v]

    # Let's start with the smallest factor.
    factors = tuple(sorted(prune_dict(phrase_v, factors)))

    # Not sure what we are doing in this function, but this
    # test prevents strange things happening if we get here
    # by mistake.
    if not factors:
        root = False
        return

    smallest_factor = factors[0]

    # First, test to see if there can be any further factoring
    # to do.
    if phrase_v in dead_ends:
        return matches

    if smallest_factor*smallest_factor > phrase_v:
        dead_ends.add(phrase_v)
        return matches

    # There may be something here. Let's look.
    try:
        for factor in factors:
            stats.tries += 1

            # Tree pruning takes place here in two steps.
            # At depth == 0, we add this factor to the list of seen factors,
            #   and set the current_root to the current factor.
            # if not depth:
            if depth in (0, 1):
                stats.nodes += 1
                logger.debug(f"root {factor=}")
                seen_roots.add(factor)
                current_root = factor

            # We consider whether we have already seen this
            # factor at a lower depth, provided it is not the current root
            # of this subtree. This guards against the case in which the
            # same factor might appear twice or more in a word
            # like "cancan."
            elif factor in seen_roots and factor - current_root:
                logger.debug(f"skipping {factor}")
                continue

            # For clarity.
            else:
                pass

            # Note that we are not checking the timeout every trip through
            # the loop --- just each new factor at the root level.
            if depth in (0, 1):
                elapsed = round(time.time() - start_time, 3)
                if elapsed > time_out:
                    sys.stderr.write(f"{time_out=} exceeded.\n")
                    sys.exit(os.EX_CONFIG)
                else:
                    sys.stderr.write(' ' * 40)
                    sys.stderr.write('\r')
                    sys.stderr.write(f"{elapsed} : {len(seen_roots)}\r")


            residual = phrase_v // factor
            if residual in factors: # Found one.
                logger.debug(f"found terminal: {residual}")
                root[factor] = residual

            elif residual < smallest_factor: # This is a dead-end.
                logger.debug(f"deadend: {residual}")
                dead_ends.add(residual)

            else: # We don't yet know.
                logger.debug(f"recursing with {residual}")
                if (t := find_words(residual,
                        tuple(_ for _ in factors if _ < residual),
                        depth+1)):

                    root[factor] = t

    except Exception as e:
        logger.error(str(e))
        raise

    finally:
        return root


@trap
def prune_dict(filter:int,
    candidates:tuple) -> tuple:
    """
    This is function just for clarity
    """
    return tuple(k for k in candidates if not filter % k)


@trap
def anagrammar_main(myargs:argparse.Namespace) -> int:
    """
    Let's build the anagram tree.

    myargs  -- from the command line.

    returns -- an int from os.EX_*
    """
    global prime_map
    global tries
    global time_out
    global topline
    global smallest_word
    global words

    # If we have been given a limit on CPU, set it.
    time_out = myargs.cpu_time

    # We cannot work without a dictionary, so let's get it first.
    words, prime_map = dictloader(myargs.dictionary)
    logger.info(f"Dictionary of {len(words)} words.")
    logger.info(f"{prime_map=}")

    # Always be nice. Each level of niceness lowers the priority
    # by 10%, so this will roughly cut the CPU proportion to about 1/2
    # of what it was.
    os.nice(myargs.nice)

    original_words = [ _ for _ in myargs.phrase.lower() if _ in string.ascii_lowercase ]
    original_phrase = "".join(original_words)
    original_phrase_value = word_value(original_phrase)

    # smallest_word is a little bit of a misnomer. It is the word
    # with the lowest possible numeric value. Let's initialize
    # it as the product of the first n primes, where n is the
    # min_len of the words we are considering.
    min_len  = myargs.min_len

    logger.info(f"{myargs.phrase=}")
    # The only words we need to consider are the ones that divide
    # the target phrase evenly. This operation greatly reduces
    # the size of the dictionary.
    words = {k:v for k, v in words.items() if len(v[0]) >= myargs.min_len and
        original_phrase_value % k == 0}
    stats.factors = len(words)
    smallest_word = min(words) if words else 0
    largest_word = max(words) if words else 0

    logger.info(f"Initial pruning for {original_phrase_value=} {len(words)=}")
    logger.debug(f"{smallest_word=}")
    logger.debug(f"{largest_word=}")

    # Let's reduce the complexities of dragging around the dictionary, and
    # just leave it here for later review. We'll figure out which words
    # correspond to the factors when we return with the anagrams.
    anagrams = SloppyTree()
    try:
        anagrams[original_phrase_value] = find_words(original_phrase_value,
                                                    tuple(sorted(words.keys())))

    except KeyboardInterrupt as e:
        print("You pressed control C")
        sys.exit(os.EX_OK)

    except Exception as e:
        logger.error(f"Unexpected exception {e=}")
        raise e from None

    finally:
        logger.debug(f"1 {anagrams=}")

    stats.dead_ends = len(dead_ends)

    ###
    # The anagrams are now in a tree whose root node is our
    # original phrase, and whose branches represent the anagrams.
    # Each path to a leaf is an anagram.
    #
    # SloppyTree.tree_as_table() returns each path as a tuple.
    # We need to sort each path so that we eliminate unintended
    # duplicates of the forms (a,b,c) and (a,c,b), and then
    # sort the sorted tuples.
    #
    # Explanation of the next line:
    #   We don't care to have each anagram start with the original phrase,
    #   so chop it off with the [1:] slice.
    ###
    anagrams = [ sorted(_)[:-1] for _ in anagrams.tree_as_table() ]
    logger.debug(f"2 {anagrams=}")

    ###
    # Use groupby to remove duplicates from the (already) now sorted list
    # of anagrams.
    ###
    anagrams = [ list(_)[0] for k, _ in itertools.groupby(sorted(anagrams)) ]
    logger.debug(f"3 {anagrams=}")

    ###
    # Now replace the numbers with the corresponding words
    # from the dictionary. Note that words.get() will return
    # None if this path is a dead-end.
    ###
    text_anagrams = []
    for gram in anagrams:
        text_gram = [ words.get(_) for _ in gram ]
        if None in text_gram: continue
        text_anagrams.append(text_gram)

    for i, line in enumerate(text_anagrams):
        if None in line: continue
        print(f"{i} :: {line}")

    print(f"{stats=}")

    return sys.exit(os.EX_OK)


if __name__ == "__main__":

    vm_callable = f"{os.path.basename(__file__)[:-3]}"
    logfile     = f"{vm_callable}.log"
    main        = f"{vm_callable}_main"
    configfile  = f"{vm_callable}.toml"

    parser = argparse.ArgumentParser(prog="anagrammar",
        description="A brute force anagram finder.")

    parser.add_argument('-d', '--dictionary', type=str, default="words",
        help="Name of the dictionary of words, or a pickle of the dictionary.")
    parser.add_argument('-m', '--min-len', type=int, default=3,
        help="Minimum length of any word in the anagram. The default is 3.")
    parser.add_argument('--nice', type=int, choices=range(0, 20), default=7,
        help="Niceness may affect execution time. The default is 7, which is about twice as nice as the average program.")
    parser.add_argument('-t', '--cpu-time', type=float, default=60,
        help="Set a maximum number of CPU seconds for execution.")
    parser.add_argument('-v', '--verbose', type=int, default=35,
        help=f"Set the logging level on a scale from {logging.DEBUG} to {logging.CRITICAL}. The default is 35, which only logs errors.")
    parser.add_argument('-z', '--zap', action='store_true',
        help="If set, remove old logfile[s].")

    parser.add_argument('phrase', type=str,
        help="The phrase. If it contains spaces, it must be in quotes.")

    myargs = parser.parse_args()
    if myargs.zap:
        try:
            os.unlink(logfile)
        except:
            pass

    try:
        with open(configfile, 'rb') as f:
            config=tomllib.load(f)
    except FileNotFoundError as e:
        config={}

    logger = urlogger.URLogger(logfile=logfile, level=myargs.verbose)
    logger.info(dump_cmdline(myargs))

    sys.exit(globals()[main](myargs))
