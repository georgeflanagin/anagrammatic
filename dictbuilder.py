#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import typing
from   typing import *

import os
import sys

import collections
from   collections import defaultdict
import gc
import math
import pickle
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

two_letter_words = frozenset({
    'am', 'an', 'as', 'at', 'be', 'by', 'do', 'go',
    'he', 'if', 'in', 'is', 'it', 'me', 'my', 'no',
    'of', 'om', 'on', 'or', 'ox', 'pi', 'so', 'to',
    'up', 'us', 'we'
    })


@trap
def dictbuilder(infile:str, outfile:str, **kwargs) -> int:
    """
    Transform the usual layout system dictionary into a picked
    version of the same. 

    infile  -- the file we read.
    outfile -- the results. This is a stem-name to which we will
        append '.forward' and '.reversed'
    kwargs  -- options that control what dictionary words are
        in and out.

        "propernouns" -- if True, do not discard capitalized words,
            and if a string, assume it is the name of a dictionary
            of proper nouns to be added. 

    This code is written to enable option processing. It is not
    particularly efficient because it is only executed once.
    """

    with open(infile) as in_f:
        data = in_f.read().split()
    sys.stderr.write(f"{len(data)} words read from {infile}.\n")

    ###
    # Apply filters
    ###
    if 'propernouns' not in kwargs:
        sys.stderr.write("removing proper nouns\n")
        data = [ _ for _ in data if _.islower() ]
        sys.stderr.write(f"{len(data)} words remain")
    
    elif kwargs['propernouns'] is not True:
        with open(kwargs['propernouns']) as f:
            nouns = f.read().lower().split()
        print(f"{len(nouns)} nouns added.")
        data = data + nouns

    else:
        pass # add more switches here.

    ###
    # Now we start creating our data structures. Always leave out
    # words with embedded punctuation and numerals.
    ###
    filtered_data = {k.lower(): "".join(sorted(k.lower())) 
        for k in data if k.isalpha() }
    sys.stderr.write(f"{len(filtered_data)} words remain after filtering.")

    ###
    # reverse this dictionary.
    ###
    reversed_dict = collections.defaultdict(list)
    for _ in set(list(filtered_data.keys())):
        reversed_dict[filtered_data[_]].append(_)
    sys.stderr.write(f"reversed dict has {len(reversed_dict)} keys.\n")
    ###
    # the dictionary cannot change once it is built, so convert the lists
    # of strings that are the values to tuples of strings. Saves space,
    # and increases usefulness because tuples are hashable and lists 
    # are not.
    ###
    reversed_dict = { k : tuple(v) for k, v in reversed_dict.items() }

    with open(f"{outfile}.reversed", 'wb') as out:
        pickle.dump(reversed_dict, out)
        sys.stderr.write("reversed dict pickled and written\n")

    with open(f"{outfile}.forward", 'wb') as out:
        pickle.dump(filtered_data, out)
        sys.stderr.write("forward dict pickled and written\n")

    return len(reversed_dict)
        

def dictloader(filename:str) -> tuple:
    """
    read the pickled dictionaries from files whose name
    matches the argument, and with .forward and .reversed 
    appended to the name.

    returns -- forward, reversed
    """

    with open(f"{filename}.forward", 'rb') as f:
        forward_dict = pickle.load(f)

    with open(f"{filename}.reversed", 'rb') as f:
        reversed_dict = pickle.load(f)

    return forward_dict, reversed_dict
