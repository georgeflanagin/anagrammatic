#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import typing
from   typing import *

import os
import sys

import argparse
import collections
from   collections import defaultdict
import gc
import math
import platform
import pickle
import pprint
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


this_os = platform.system()
if this_os == 'Linux':
    default_word_list = '/usr/share/dict/linux.words'
elif this_os == 'Darwin':
    default_word_list = '/usr/share/dict/words'
else:
    default_word_list = './words'

###
# The alphabet order is not relevant to the algorithm. This order
# was chosen to reduce the magnitude of the numbers slightly.
###
primes = dict(zip("eariotnslcudpmhgbfywkvxzjq", (2, 3, 5, 7, 11, 
    13, 17, 19, 23, 29, 
    31, 37, 41, 43, 47, 
    53, 59, 61, 67, 71, 
    73, 79, 83, 89, 97,
    101 )))

def word_value(word:str) -> int:
    return math.prod(primes[_] for _ in word)

one_letter_words = frozenset({'a', 'i'})


two_letter_words = frozenset({
    'am', 'an', 'as', 'at', 'be', 'by', 'do', 'go',
    'he', 'if', 'in', 'is', 'it', 'me', 'my', 'no',
    'of', 'om', 'on', 'or', 'ox', 'pi', 'so', 'to',
    'up', 'us', 'we'
    })


three_letter_words = frozenset({
    "aaa", "aas", "afa", "aff", "aga", "ags", "aha", "ahi", "ahs",
    "aid", "ail", "aim", "ain", "air", "ais", "ait", "ake", "ala",
    "alb", "ale", "all", "alp", "als", "alt", "ama", "ami", "amp",
    "ana", "and", "ane", "ani", "ant", "any", "ape", "apo", "app",
    "apt", "arb", "arc", "ard", "are", "arf", "ark", "arm", "art",
    "ash", "ask", "asp", "ate", "att", "auk", "aul", "ava", "ave",
    "avo", "awa", "awl", "awn", "axe", "ayr", "ays", "azo", "bag",
    "bak", "bal", "bam", "ban", "bap", "bas", "bat", "bay", "baz",
    "bee", "beg", "bel", "bes", "bet", "bey", "bib", "bid", "big",
    "bim", "bio", "bis", "bit", "biz", "bod", "bog", "Boi", "bok",
    "boo", "bop", "bos", "bot", "bov", "bow", "box", "boy", "bro",
    "brr", "bub", "bud", "bug", "bum", "bun", "bur", "bus", "but",
    "buy", "bye", "bys", "cab", "cad", "cam", "can", "cap", "car",
    "caw", "cay", "cee", "cep", "chi", "cig", "cis", "cob", "cod",
    "cog", "col", "cop", "cor", "cos", "cow", "cox", "coy", "coz",
    "cru", "cry", "cub", "cud", "cue", "cup", "cur", "cut", "cwm",
    "dab", "dad", "dag", "dah", "dak", "dal", "dan", "dap", "dat",
    "dau", "daw", "day", "deb", "dee", "def", "deg", "del", "den",
    "dev", "dew", "dex", "dey", "dib", "did", "dif", "dip", "dir",
    "dis", "dit", "div", "dob", "doc", "doe", "doh", "dol", "dom",
    "don", "doo", "dop", "dor", "dos", "dot", "dow", "dry", "dub",
    "dud", "due", "dug", "duh", "dui", "dun", "duo", "dup", "dux",
    "dye", "dzo", "ear", "eat", "eau", "ebb", "ecu", "edh", "eds",
    "eek", "eel", "eep", "eet", "eff", "efs", "eft", "egg", "eid",
    "eke", "eld", "elf", "elk", "ell", "elm", "els", "eme", "emo",
    "ems", "emu", "end", "eng", "ens", "ent", "eon", "era", "ere",
    "erk", "ern", "err", "ers", "esh", "esp", "ess", "eta", "eth",
    "ety", "eve", "ewe", "exy", "eye", "fab", "fad", "fag", "fah",
    "fan", "fap", "fas", "fat", "fax", "fay", "fed", "fee", "feh",
    "fem", "fen", "fer", "fes", "fet", "feu", "few", "fey", "fez",
    "fib", "fid", "fie", "fig", "fil", "fir", "fit", "fix", "fiz",
    "flu", "fly", "fob", "foe", "fog", "foh", "fon", "foo", "fop",
    "for", "fou", "fox", "foy", "fro", "fry", "fub", "fud", "fug",
    "fun", "fur", "gab", "gad", "gae", "gag", "gal", "gam", "gan",
    "gap", "gar", "gas", "gat", "gau", "gaw", "gay", "ged", "gee",
    "gel", "gem", "gen", "get", "gey", "ghi", "gib", "gid", "gie",
    "gig", "gin", "gip", "git", "gnu", "goa", "gob", "god", "gog",
    "gom", "gon", "goo", "gor", "gos", "got", "gox", "goy", "gry",
    "gul", "gum", "gun", "gut", "guv", "guy", "gym", "gyp", "had",
    "hae", "hag", "hah", "haj", "ham", "han", "hao", "hap", "har",
    "has", "hat", "haw", "hay", "hed", "heh", "hem", "hen", "hep",
    "hes", "het", "hew", "hex", "hey", "hic", "hid", "hie", "him",
    "hin", "hip", "hir", "his", "hit", "hmm", "hob", "hoe", "hon",
    "hop", "hor", "hot", "hov", "how", "hoy", "hub", "hue", "hug",
    "huh", "hum", "hun", "hup", "hyp", "ice", "ick", "icy", "ide",
    "ids", "iff", "ifs", "igg", "ile", "ilk", "ill", "imp", "ink",
    "inn", "ins", "int", "ion", "ipe", "ire", "irk", "ish", "ism",
    "isu", "its", "ivy", "jab", "jag", "jam", "Jap", "jar", "jaw",
    "jay", "jee", "jeg", "jer", "jet", "jeu", "jew", "jib", "jig",
    "jin", "job", "joe", "jog", "jot", "jow", "joy", "jug", "jun",
    "jus", "jut", "kab", "kae", "kaf", "kas", "kat", "kaw", "kay",
    "kea", "kef", "keg", "ken", "kep", "ket", "kex", "key", "khi",
    "khu", "kid", "kif", "kim", "kip", "kir", "kis", "kit", "koa",
    "kob", "koi", "kop", "kor", "kos", "kot", "kue", "kut", "kye",
    "lab", "lac", "lad", "lag", "lah", "lai", "lam", "Lao", "lap",
    "lar", "lat", "lav", "law", "lax", "lbs", "lea", "led", "lee",
    "leg", "lei", "lek", "les", "let", "leu", "lev", "lex", "ley",
    "lez", "lib", "lid", "lie", "lil", "lip", "lis", "lit", "log",
    "lol", "loo", "lop", "lot", "lug", "lum", "Luo", "luv", "lux",
    "lye", "mac", "mae", "mal", "mam", "man", "mar", "mat", "maw",
    "max", "may", "med", "meg", "meh", "mel", "mem", "men", "met",
    "meu", "mew", "mho", "mia", "mib", "mic", "mid", "mig", "mil",
    "mim", "min", "mir", "mis", "mix", "moa", "mob", "moc", "mod",
    "mog", "moi", "mol", "mom", "mon", "moo", "mop", "mor", "mos",
    "mot", "mow", "mud", "mug", "mum", "mus", "mut", "mux", "myc",
    "naa", "nab", "nae", "nag", "nah", "nam", "nan", "nap", "naw",
    "nay", "neb", "ned", "nee", "neg", "nen", "net", "neu", "new",
    "nib", "nid", "nil", "nip", "nit", "nix", "nob", "nod", "nog",
    "noh", "nom", "non", "noo", "nor", "nos", "not", "nth", "nub",
    "num", "nun", "nus", "nut", "oaf", "oak", "oar", "oat", "oba",
    "obe", "obi", "oca", "oda", "ode", "ods", "oes", "oft", "ohi",
    "ohm", "ohs", "oik", "oil", "oka", "oke", "old", "ole", "olf",
    "olm", "oms", "omy", "one", "ono", "ons", "ooh", "oot", "ope",
    "ops", "opt", "ora", "orb", "orc", "ord", "ore", "org", "ors",
    "ort", "ose", "oud", "our", "out", "ova", "owe", "owl", "own",
    "owt", "oxo", "oxy", "pac", "pal", "pam", "pan", "pap", "par",
    "pas", "pat", "pav", "paw", "pax", "pea", "pec", "ped", "pee",
    "peh", "pep", "per", "pes", "pew", "phi", "pht", "pia", "pic",
    "pie", "pig", "pip", "pis", "pit", "piu", "ply", "pod", "poh",
    "poi", "pol", "pom", "poo", "pop", "pot", "pov", "pow", "pro",
    "pry", "psi", "pst", "pub", "pud", "pug", "pul", "pun", "pup",
    "pur", "pus", "put", "pwn", "pya", "pye", "pyx", "qat", "qis",
    "qua", "rad", "rag", "rah", "rai", "raj", "ram", "ran", "rap",
    "ras", "rat", "raw", "rax", "ray", "reb", "rec", "ree", "ref",
    "reg", "rei", "rem", "ren", "rep", "res", "ret", "rev", "rex",
    "rez", "rho", "ria", "rib", "rid", "rif", "rig", "rin", "rip",
    "rob", "roc", "rod", "rog", "rom", "roo", "rot", "row", "rub",
    "rue", "rug", "rum", "run", "rut", "rya", "sab", "sac", "sae",
    "sag", "sai", "sal", "sam", "sap", "sat", "sau", "sav", "saw",
    "sax", "say", "sea", "sec", "sed", "see", "seg", "sei", "sel",
    "ser", "set", "sew", "sex", "sha", "she", "shh", "shy", "sib",
    "sic", "sim", "sip", "sir", "sis", "six", "ska", "ski", "sky",
    "sly", "sod", "soh", "sol", "som", "son", "sop", "sos", "sot",
    "sou", "sov", "sow", "sox", "soy", "soz", "spa", "spy", "sri",
    "ssh", "sss", "sty", "sub", "sue", "suk", "sum", "sun", "sup",
    "suq", "syn", "taa", "tab", "tad", "tae", "tag", "taj", "tam",
    "tan", "tao", "tap", "tar", "tas", "tat", "tau", "tav", "taw",
    "tax", "tea", "ted", "teg", "teh", "ten", "tet", "tew", "tey",
    "tho", "thy", "tia", "tib", "tic", "tie", "tik", "tip", "tis",
    "tit", "tod", "toe", "tog", "tom", "ton", "too", "top", "tor",
    "tot", "tow", "toy", "try", "tsk", "tub", "tug", "tui", "tum",
    "tun", "tup", "tut", "tux", "twa", "two", "tye", "udo", "uey",
    "ugh", "uke", "ulu", "ume", "umm", "ump", "uni", "uns", "upo",
    "ups", "urb", "urd", "urn", "urp", "use", "uta", "uts", "uzi",
    "vac", "van", "var", "vas", "vat", "vau", "vav", "vaw", "vee",
    "veg", "ven", "vet", "vex", "via", "vid", "vie", "vig", "vim",
    "vis", "voe", "vog", "vol", "vom", "vow", "vox", "vug", "vum",
    "wab", "wad", "wae", "wag", "wai", "wan", "wap", "war", "was",
    "wat", "waw", "way", "web", "wed", "wee", "wem", "wen", "wet",
    "wey", "wha", "who", "why", "wid", "wif", "wig", "wis", "wit",
    "wiz", "woe", "wok", "won", "woo", "wop", "wos", "wot", "wow",
    "wry", "wud", "wye", "wyn", "xis", "xor", "yag", "yah", "yak",
    "yam", "yap", "yar", "yaw", "yay", "yea", "yeh", "yem", "yen",
    "yep", "yes", "yet", "yew", "yex", "yin", "yip", "yob", "yod",
    "yok", "yom", "yon", "yow", "yuk", "yum", "yup", "yus", "zag",
    "zak", "zap", "zas", "zed", "zee", "zek", "zen", "zep", "zho",
    "zib", "zig", "zin", "zip", "zit", "zoa", "zoe", "zoo", "zun",
    "zuz", "zzz"
    })

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
def dictbuilder(myargs:argparse.Namespace) -> int:
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

    returns -- a value from the os.EX_ family of return codes.

    This code is written to enable option processing. It is not
    particularly efficient because it is only executed once.
    """

    global two_letter_words
    global three_letter_words

    data = []
    infile = myargs.input
    with open(infile) as in_f:
        data.extend(in_f.read().split())
    sys.stderr.write(f"{len(data)} words read from {infile}.\n")


    if not myargs.bare:
        # Let's use /our/ three and two letter words, Knuth's
        # five letter words, and the Scrabble dictionary's four letter words.
        data = [ _ for _ in data if len(_) > 5 ]
        with open('./knuths.5757.five.letter.words.txt') as in_f:
            five_letter_words = in_f.read().split()
        data.extend(five_letter_words)
        with open('./four.letter.words') as in_f:
            four_letter_words = in_f.read().split()
        data.extend(four_letter_words)

        print("Adding short words from internal list.")
        data.extend(three_letter_words) 
        data.extend(two_letter_words)
        data.extend(('a', 'i'))
        print(f"{len(data)} words ready for filtering.")

    ###
    # Apply filters
    ###
    if myargs.propernouns:
        # First remove the capitalized words from what we have
        # already read in.
        sys.stderr.write("removing proper nouns\n")
        data = [ _ for _ in data if _.islower() ]
        print(f"{len(data)} words remain after removing proper nouns.")
    
        with open(myargs.propernouns) as f:
            nouns = set(f.read().lower().split())
        data = set(data) - nouns


    ###
    # Now we start creating our data structures. Always leave out
    # words with embedded punctuation and numerals.
    ###
    filtered_data = {k.lower(): "".join(sorted(k.lower())) 
        for k in data if k.isalpha() }
    print(f"{len(filtered_data)} words remain after isalpha() filtering.")

    ###
    # Our collection of words has integer keys that correspond to
    # a composite number that represents the values of each letter
    # multiplied together, and a tuple of words that have the same
    # factorization. For example:
    #
    # care = 5 * 2 * 61 * 11 = 6710
    #
    # So, in the dictionary, we will have.
    #
    # { 6710 : ('care', 'race', 'acre') }
    ###
    words = collections.defaultdict(list)
    for word in filtered_data:
        words[word_value(word)].append(word)

    words = {k:tuple(v) for k, v in words.items()}


    with open(f"{myargs.outfile}.numbers", 'wb') as out:
        pickle.dump(words, out)
        sys.stderr.write("forward dict pickled and written\n")

    with open(f"{myargs.outfile}.txt", 'w') as out:
        out.write(pprint.pformat(words))


    return len(words)
        

def dictloader(filename:str) -> dict:
    """
    read the pickled dictionaries from files whose name
    matches the argument, and with .forward and .reversed 
    appended to the name.

    returns -- forward, reversed
    """
    if filename.endswith('.'): filename = filename[:-1]

    with open(f"{filename}.numbers", 'rb') as f:
        numeric_dict = pickle.load(f)

    return numeric_dict


if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog="dictbuilder", 
        description="A program to maintain dictionaries used in anagrammar.")

    parser.add_argument('-d', '--bare', action='store_true',
        help="Use only the words in the input dictionary rather than the built-in 2, 3, 4, and 5 letter words.")
    parser.add_argument('-i', '--input', type=str, 
        required=True, help="The name[s] of the input dictionaries.") 
    parser.add_argument('-n', '--propernouns', type=str, default=None,
        help="If used, exclude the words found in the file (presumed to be proper nouns)")
    parser.add_argument('outfile', type=str,
        help="Name of the dictionary to be written (minus the suffixes).")

    myargs = parser.parse_args()
    dump_cmdline(myargs)

    sys.exit(dictbuilder(myargs))
