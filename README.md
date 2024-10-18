# anagrammar

A brute force anagram finder, a teaching tool, and a one gram pun.
For more information, please consult [Lisa
Simpson](https://www.youtube.com/watch?v=cj71HnSJaUM).

## How did this program come to be?

A number of people with whom I work use the [Internet Anagram
Server](https://new.wordsmith.org/anagram/), and apparently we are not alone.
It seems always to be down or overwhelmed by requests. To minimize
its CPU usage, it works with a small list of common words. I'm
interested in more interesting words.

For example, `embrace inclusivity` is an anagram for 

- `unmiscable veracity`
- `cystic nerve bulimia`

and a few other phrases --- but who knew?

Anagrams are an example of a *perfect cover* problem, as described in
Knuth Vol 4B, pages 66 ff. A perfect cover is a collection of non-empty,
disjoint sets whose union is the target set we are trying to "cover." 
Knuth calls the subsets *options* and the elements of each option are
*items*. Thus, no item is a member of more than one option.

One of the subtle and confusing complications of anagrams is that an
item (letter) may appear in more than one option (word), and for a 
cover (phrase) to be considered complete, it must use all instances of
a repeated item. In the example above `embrace inclusivity` has three
items whose value is i. We are trying to cover this set:

`['a', 'b', 'c', 'c', 'e', 'e', 'i', 'i', 'i', 
  'l', 'm', 'n', 'r', 's', 't', 'u', 'v', 'y']`

not this one 

`['a', 'b', 'c', 'e', 'i',  'l', 'm', 
   'n', 'r', 's', 't', 'u', 'v', 'y']`

The approach taken in this program is a weakened implementation of 
Knuth's *Algorithm X*, described in detail in 
[this 2000 paper](https://www.ocf.berkeley.edu/~jchu/publicportal/sudoku/0011047.pdf), and
in summary form in the [Wikipedia article](https://en.wikipedia.org/wiki/Knuth%27s_Algorithm_X).

Anagrammar's approach is identical: each option (word) we examine is removed 
as we go, and we are left with a smaller exact cover problem, the remainder. If we 
are eventually left with a null set, then we have found an anagram. 
The options are construed to be words in some dictionary, and if 
our residual (Knuth's term) cannot be spanned by the remaining options, then this
branch was a dead end, and we go back to consider other options.

I borrowed the primitive calculations from Martin Schweitzer (@martinschweitzer on github) by
assigning the letters of the alphabet to the 26 smallest prime numbers. This 
legerdemain eliminated the shuffling and sorting of the letters through string
operations, and the entire calculation is reduced to integer arithmetic. If 
this approach is unfamiliar, five minutes spent reviewing [the fundamental 
theorem of arithmetic](https://en.wikipedia.org/wiki/Fundamental_theorem_of_arithmetic) 
will clear it up for you. 


Of course, anagrams differ from the basic perfect cover problem in 
other material ways. The first is that we are not looking for just
one anagram --- we want to find them all. The second is that nearly 
every combination of two and three letters has been used as an acronym
for something in English, for example, TLA -- Three Letter Acronym. We 
must be careful to exclude some of these non-word words.

If you read about *Algorithm X* you will notice that Knuth starts out by 
saying that one should consider the smallest option first, and from several
such options all of equal size, the selection can be made arbitrarily. 
The implementation choice to represent each option as a composite integer 
that stands for a dictionary word has the advantage that it is easy (and 
deterministic) to start
with the ``smallest'' option, and easy to sort the options by size.

In the case of anagrams, several words may map onto the same option


## What do you need to run it?

*A standard distro of Python.* This program does not use external
libraries, and the source is cut into a few files simply to give
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
                  [--nice {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19}] [-t CPU_TIME] [-v VERBOSE] [-z]
                  phrase

A brute force anagram finder.

positional arguments:
  phrase                The phrase. If it contains spaces, it must be in quotes.

options:
  -h, --help            show this help message and exit
  -d DICTIONARY, --dictionary DICTIONARY
                        Name of the dictionary of words, or a pickle of the dictionary.
  -m MIN_LEN, --min-len MIN_LEN
                        Minimum length of any word in the anagram. The default is 3.
  --nice {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19}
                        Niceness may affect execution time. The default is 7, which is about twice as nice as
                        the average program.
  -t CPU_TIME, --cpu-time CPU_TIME
                        Set a maximum number of CPU seconds for execution.
  -v VERBOSE, --verbose VERBOSE
                        Set the logging level on a scale from 10 to 50. The default is 35, which only logs
                        errors.
  -z, --zap             If set, remove old logfile[s].

```

### Start with something small.

How about *george flanagin* as the phrase? First, source the `anagram.bash` 
file, and you will then be able to just type `anagram` to run the program. The 
output will appear on the screen, which is not always useful if there are a lot
of anagrams to your phrase.

Here is what the output looks like when we route the anagrams to `gkf.txt`.

```
anagram -d words -m 3 georgeflanagin > gkf.txt
 --cpu-time 60 --dictionary words --min-len 3 --nice 7 --phrase georgeflanagin --verbose 35 --zap False

0.857 : 262144
1.496 : 524288
2.031 : 786432
2.42user 0.03system 0:02.46elapsed 99%CPU (0avgtext+0avgdata 110416maxresident)k
0inputs+6968outputs (0major+24128minor)pagefaults 0swaps
```

In the `gkf.txt` file, the most interesting anagram to me is `long fearing age`,
and at the bottom of the file we see the "stats:"

```
Tree had 194092 paths.
Tree had 39147 distinct paths.
tries=803821 deadends=414962
```

The apparent speed is mainly due to running the program on a reasonably
fast CPU. The big number, `803821`, is the number of edges in the 
exhaustive graph. `414962` is the number of edges whose leaves are 
a value (combination of letters) that do not spell a word in the dictionary.
After the removing the dead-end edges, there were `194092` paths (NOTE: a path
consists of at least one edge, but generally more.) from the root to a valid
leaf.
Of course, many are duplicates: *long -> fearing -> age* is the same as 
*age -> long -> fearing*. After removing the duplicates,
there were only `39147` anagrams of the original phrase.

You will notice in the output that the results are written this way, one
anagram per line.

```python
(('fragile',), ('gag',), ('enon', 'neon', 'none'))
```

Many small groups of characters spell more than one word, such
as `('enon', 'neon', 'none')`, and this allows for a more 
compact representation than something like:

```python
('fragile', 'gag', 'enon')
('fragile', 'gag', 'neon')
('fragile', 'gag', 'none')
```

## Trivia Q & A.

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

