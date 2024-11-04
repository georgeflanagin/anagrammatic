# anagrammar

A brute force anagram finder, a teaching tool, and a one gram pun.
For more information, please consult [Lisa
Simpson](https://www.youtube.com/watch?v=cj71HnSJaUM).

## Anagrams? Seriously?

A number of people with whom I work use the [Internet Anagram
Server](https://new.wordsmith.org/anagram/), and apparently we are not alone.
It seems always to be down or overwhelmed by requests. To minimize
its CPU usage, it works with a small list of common words. I'm
interested in more interesting words.

For example, `embrace inclusivity` is an anagram for 

- `unmiscable veracity`
- `cystic nerve bulimia`

and a few other phrases --- but who knew?

As a member of University of Richmond's professional staff, I am in continual
need of classroom and workshop examples that show the solutions, complete or
approximate, to classic computer science problems. Because it is difficult to find such 
examples in the wild, I usually write my own. 

I take this moment to credit and thank my former intern
[Alina Enikeeva](https://www.linkedin.com/in/alina-enikeeva), now a consulting engineer with 
[RTS Labs](https://rtslabs.com/), for adding convenience 
iterators to the underlying tree data structure, and class of 2025 intern
[Skyler He](https://www.linkedin.com/in/yingxinskylerhe/) for her **extensive** proofreading of the code and development
of test cases.

## How does it work?

Anagrams are an example of a *exact cover* problem, as described in Knuth's
[*The Art of Computer Programming*, 
Combinatorial Algorithms, Part 2](https://www.amazon.com/Art-Computer-Programming-Combinatorial-Information/dp/0201038064/), 
pages 66 ff. This book is often referred to as simply "4B." 
An exact cover (alternatively: *perfect cover*) is a collection of non-empty,
disjoint sets whose union is the target set we are trying to "cover." 
Knuth calls the subsets *options* and the elements of each option are
*items*. Thus, no item occurs more than once in an option, and no
item appears in more than one option in any single cover.

One of the subtle and confusing complications of anagrams is that an
item (letter) may appear in more than once in an option (word). For a 
cover (phrase) to be considered complete, it must use all instances of
a repeated item. In the example above `embrace inclusivity` has three
items whose value is *i*, two whose value is *c*, and two whose value is *e*. 
We are trying to cover this set:

`['a', 'b', 'c', 'c', 'e', 'e', 'i', 'i', 'i', 
  'l', 'm', 'n', 'r', 's', 't', 'u', 'v', 'y']`

not this one 

`['a', 'b', 'c', 'e', 'i',  'l', 'm', 
   'n', 'r', 's', 't', 'u', 'v', 'y']`

The approach taken in this program is a modified implementation of 
Knuth's *Algorithm X*, described in detail in 
[this 2000 paper](https://www.ocf.berkeley.edu/~jchu/publicportal/sudoku/0011047.pdf), and
in summary form in the [Wikipedia article](https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X).
Algorithm X is a part of *backtracking*, an important class of algorithms
that are summarized [here](https://en.wikipedia.org/wiki/Backtracking).

Anagrammar's approach is straightforward exploitation of Algorithm X: 
each option (word) we examine is removed 
as we go, and we are left with a smaller exact cover problem. If we 
are eventually left with a null set, then we have found an exact cover (anagram). 
The options are construed to be words in some dictionary, and if 
our residual (Knuth's term for the remainder) cannot be spanned by the remaining options, then this
branch was a dead end, and we go back to consider other options.

I borrowed the lowest level representation from Martin Schweitzer (@martinschweitzer) by
assigning the letters of the alphabet to the 26 smallest prime numbers. This 
legerdemain eliminated the string
operations, and the entire analysis is reduced to integer arithmetic --- something that
computers are known to be good at. If 
the approach is unfamiliar, no more than five minutes spent reviewing [the fundamental 
theorem of arithmetic](https://en.wikipedia.org/wiki/Fundamental_theorem_of_arithmetic) 
will clear it up. 

In the `anagrammar.py` file, the mapping is represented this way:

```python
primes26 = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 
    43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101 )
primes = dict(zip("eariotnslcudpmhgbfywkvxzjq", primes26))
```

The ordering of the letters in alignment with the frequency of letters in
English reduces the magnitude of the composite numbers that represent
options, although experience has shown that because the factors of the 
large composite numbers are comparatively small, the `divmod` operation goes 
quickly even with a less optimized mapping. For example, our test phrase (`embrace inclusivity`) 
maps to
**695823563878969513260**, which is greater than **2**<sup>69</sup>, whereas a word
like `race` which might be a component of an anagram maps to only **870**,
not even **2**<sup>10</sup>. 

The above ordering goes one step farther, as it is an empirical
analysis of the frequency of letters in the Linux dictionary rather than some
corpus of English. We
need not concern ourselves with how *common* a word is, only that it appears
exactly *once* in any single dictionary.

The above mapping is optimized for each list of words when the `dictbuilder`
is used. The resulting dictionary has not only the words and values, but also
contains the optimum assignment of each letter to a prime number so that
the resulting values are as small as possible. 

Of course, anagrams differ from the basic perfect cover problem in 
other material ways. The first is that we are not looking for just
one cover/anagram --- we want to find them all. The second is that nearly 
every combination of two and three letters has been used as an acronym
for something in English, for example, **TLA** -- **T**hree **L**etter **A**cronym. We 
must be careful to exclude some of these non-word words for the results to
be amusing.

When you read about *Algorithm X* you will notice that Knuth starts out by 
saying that one should consider the smallest option first, and from several
such options all of equal size, the selection can be made arbitrarily. 
The implementation choice to represent each option as a composite integer 
that stands for a dictionary word has the advantage that it is easy (and 
deterministic) to start
with the ``smallest'' option, and easy to sort the options by size. Unlike
Knuth, we never need to choose among options of equal size because the 
use of prime factors effectively creates a set that is *strictly* well-ordered
instead of merely well ordered.

Another difference between covers and anagrams is that within any anagram, several words may map onto the same option. 
These words are *self-anagrams* ---
any anagram that uses one of the words can 
freely use any of the others. For example
the title of the well known album by Miles Davis, 
[Live-Evil](https://en.wikipedia.org/wiki/Live-Evil_(Miles_Davis_album)),
contains a pair of such words. In our assignment of prime numbers to 
letters, both words map to the integer 25438 (EVIL) -> (2 * 79 * 7 * 23) along with
the words `veil`, `vile`, and `levi`. What unlikely bedfellows.

## What is in the Python files?

`anagrammar.py` --- The main program. The core is a recursive function that
implements Algorithm X.

`dictbuilder.py` --- Converts a white-space delimited file of "words" to a 
pickle of a dict where the keys are integers and the values are tuples of the
words that map to the key. The output also contains a pickle that represents
the mapping of letters to prime numbers.

`urdecorators.py` --- Contains the `@trap` decorator to assist with debugging.

`sloppytree.py` --- A general purpose data structure derived from Python's `dict` 
that creates a flexible n-ary tree. 

`urlogger.py` --- A wrapper around Python's `logging` module that makes it quite
a bit easier to use, or at least it is harder to make mistakes.

## What improvements can be made to Anagrammar's run time?

Unfortunately for anagrams, exact cover problems are difficult to attack with
parallel programming methods. There is no clear way to partition the options (words) into
subspaces (dictionaries) such that we can be assured that we do not omit covers (anagrams) that use
options from multiple spaces.

Of course, the space being covered grows rapidly as the phrase we are analyzing grows longer. 
Accepting Knuth's matrix representation,
the number of columns in the matrix is equivalent to the number of letters in
the phrase, and the number of rows is equivalent to the number of words from 
the dictionary (reduced by the live-evil-vile-veil-levi mapping noted earlier) 
that can be formed from the letters in phrase. The number of rows
converges to the number words in the dictionary as the phrase becomes longer 
and every letter in the alphabet is present. 

Anagrammar does some pruning with its backtracking, identifying dead ends
as it goes. Thus, no [terminal](https://en.wikipedia.org/wiki/Terminal_and_nonterminal_symbols) 
is evaluated more than once. Of course, constantly searching an ever growing pile of 
dead ends adds *some* overhead. This is called [memoization](https://en.wikipedia.org/wiki/Memoization).
The pruning could be slightly improved, although how much it could be improved 
is an open question. 

**NB** *The following explanation conflates the length of words with the value of integer to which
the words are mapped. Hopefully, the explanation is still clear.*

The most important pruning technique is this one. Suppose we are looking for 
anagrams for `george flanagin`. Starting with the short words, we find `age long fearing`
when using `age` as a starting point. When we get to four letter words, we examine 
`long`. There is no need to look at any word shorter than `long` because all anagrams
involving `age` have already been found when we used `age` as the starting point. There
are a few improvements that can be added at the cost of a good bit of code complexity.

## What do you need to run it?

*A standard distro of Python.* This program does not use external
libraries like `numpy`, and the source is cut into a few files simply to give
it a straightforward organization.

*A dictionary.* If you do not like the provided dictionaries (taken from the
Webster's Second International Dictionary), you can use the
`dictbuilder.py` file to create your own.  If you run the program
on Linux or Mac OS, the program should find the system dictionaries
without your having to do anything extra. I have been told that
Windows is a BYODictionary experience.

## How is it run?

### The help
```
usage: anagrammar [-h] [-d DICTIONARY] [-m MIN_LEN]
                  [--nice {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19}]
                  [-t CPU_TIME] [-v VERBOSE] [-z]
                  phrase

A brute force anagram finder.

positional arguments:
  phrase                The phrase. If it contains spaces, it must
                        be in quotes.

options:
  -h, --help            show this help message and exit
  -d DICTIONARY, --dictionary DICTIONARY
                        Name of the dictionary of words, or a pickle
                        of the dictionary.
  -m MIN_LEN, --min-len MIN_LEN
                        Minimum length of any word in the anagram.
                        The default is 3.
  --nice {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19}
                        Niceness may affect execution time. The
                        default is 7, which is about twice as nice
                        as the average program.
  -t CPU_TIME, --cpu-time CPU_TIME
                        Set a maximum number of CPU seconds for
                        execution.
  -v VERBOSE, --verbose VERBOSE
                        Set the logging level on a scale from 10 to
                        50. The default is 35, which only logs
                        errors.
  -z, --zap             If set, remove old logfile[s].


```

### Start with something small.

How about *george flanagin* as the phrase? First, source the `anagram.bash` 
file, and you will then be able to just type `anagram` to run the program. The 
output will appear on the screen, which is not always useful if there are a lot
of anagrams to your phrase.

Here is what the output looks like using the (provided) dictionary of the 30000
most common English words when we route the anagrams to `gkf.txt`.

```
anagram -d 30000. -m 3 georgeflanagin > gkf.txt
 --cpu-time 60 --dictionary 30000. --min-len 3 --nice 7 --phrase georgeflanagin --verbose 35 --zap False

0.78user 0.01system 0:00.87elapsed 92%CPU (0avgtext+0avgdata 39204maxresident)k
17624inputs+1064outputs (90major+8194minor)pagefaults 0swaps

```

In the `gkf.txt` file, the most interesting anagram to me is `long fearing age`.


You will notice in the output that the results are written this way, one
anagram per line, with the substitutions *('enon', 'neon', 'none')* elaborated.

```python
(('fragile',), ('gag',), ('enon', 'neon', 'none'))
```

This allows for a more 
compact representation than something like:

```python
('fragile', 'gag', 'enon')
('fragile', 'gag', 'neon')
('fragile', 'gag', 'none')
```

## Q & A.

### I don't like your dictionaries. How do I build one of my own?

The assumption in `dictbuilder.py` is that the input is a file of words, white
space delimited. You type in something like:

`python3 dictbuilder.py [-b] -i /path/to/your/file nameyouwanttouse`

The result will be a file named `nameyouwanttouse.numbers` that you can 
reference in your calculation as `nameyouwanttouse`. If you use the `-b` 
option, the dictionary will ignore the prebuilt lists of 3, 4, and 5 letter
words, and use exactly what is in the dictionary that you provide.

### Why are the dictionaries saved as pickles? That limits their use to Python. 

This is why God gave you the ability to fork the repo. The dictionaries are
built and read entirely within the file `dictbuilder.py`, so you can change
this. There are only about 100 lines of code that do the work. 

### Why did you not follow PEP-8 exactly? Your style is terrible. 

OK, first I have heard worse and I have committed much bigger sins.
Recently. My best professional friend once described my programming
as "entirely adequate." A written performance review once included
the words "the only thing George knows how to do is write a compiler."
Both statements are probably correct.

If it bothers you, you can experiment with
[AutoPEP8](https://pypi.org/project/autopep8/0.8/).  It is excellent.

