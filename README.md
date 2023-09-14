# anagrammar

A brute force anagram finder, a teaching tool, and a one gram pun.
For more information, please consult [Lisa
Simpson](https://www.youtube.com/watch?v=cj71HnSJaUM).

## Why did you write this program?

Because programming in Python should be fun! I frequently need
teaching examples, and this seems like a good one: the topic is
simple and familiar, with the implementation revealing some design
choices and difficulties.

A number of people with whom I work use the [Internet Anagram
Server](https://new.wordsmith.org/anagram/), and apparently we are not alone.
It seems always to be down or overwhelmed by requests. To minimize
its CPU usage, it works with a small list of common words. I'm
interested in fewer, longer, and more interesting words.

For example, `embrace inclusivity` is an anagram for 

- `unmiscable veracity`
- `cystic nerve bulimia`

and a few other phrases --- but who knew?

Many teaching examples are not all that useful for improving one's
programming. They are minimum working examples of .. something ..,
but programming is not best learned in MWE size bites, just as human
language is not learned one word at a time. If you studied Spanish
and learned that "me | gusta | la | pitón" is "to me | is pleasing
| the | python," you are never going to learn Spanish. You might as
well give up now. 

## What do you need to run it?

1. A standard distro of Python. This program does not use external
libraries, and the source is cut into a few files simply to give
it a straightforward organization.

1. If you do not like the provided dictionaries (taken from the
Webster's Second International Dictionary), you can use the
`dictbuilder.py` file to create your own.  If you run the program
on Linux or Mac OS, the program should find the system dictionaries
without your having to do anything extra. I have been told that
Windows is a BYODictionary experience.

## How about an example?

### The tuning parameters

```bash
anagrammar [-h] -d DICTIONARY [-m MIN_LEN] 
    [--nice {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19}] 
    [-t CPU_TIME] 
    [-v VERBOSE]
    [-z]
    phrase

A brute force anagram finder.

positional arguments:
  phrase                The phrase. If it contains spaces, it must be in quotes.

optional arguments:
  -h, --help            show this help message and exit
  -d DICTIONARY, --dictionary DICTIONARY
                        Name of the dictionary of words, or a pickle of the dictionary.
  -m MIN_LEN, --min-len MIN_LEN
                        Minimum length of any word in the anagram. The default is 3.
  --nice {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19}
                        Niceness may affect execution time. The default is 7, which is about twice as nice as the average program.
  -t CPU_TIME, --cpu-time CPU_TIME
                        Set a maximum number of CPU seconds for execution.
  -v VERBOSE, --verbose VERBOSE
                        Set the logging level on a scale from 10 to 50. The default is 35, which only logs errors.
  -z, --zap             If set, remove old logfile[s].
```

`-m`, `--min-len` This tells the anagrammar the shortest word to consider
when building the initial list of possible words. The default value is
`3` because a lot of anagrams with two letter words are uninteresting.

`-d`, `--dictionary` In this project, I have provided a dictionary built
from Google's list of 20,000 words.  The one named `words` is much larger,
coming from the New Webster's Dictionary that is included with Linux in
`/usr/share/dict/words`.

`-t`, `--cpu-time` The program can be caused to stop after a given number of seconds
of execution. I put this in when I was developing the program, and I never got
around to removing it.

`--verbose` Takes a number that corresponds to the loglevel. The default is
`35`, and this value eliminates almost all output.

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
reference in your calculation as `nameyouwanttouse`.

### The PDF documentation looks like it is not finished.

Yes.

### Why are the dictionaries saved as pickles? That limits their use to Python. 

This is why God gave you the ability to fork the repo. The dictionaries are
built and read entirely within the file `dictbuilder.py`, so you can change
this. There are only about 100 lines of code that do the work. 

### Why did you not follow PEP-8 exactly? Your style is terrible. 

OK, first I have heard worse and I have committed bigger sins.
Recently. My best professional friend once described my programming
as "entirely adequate." A written performance review once included
the words "the only thing George knows how to do is write a compiler."
Both statements are probably correct.

If it bothers you, you can experiment with
[AutoPEP8](https://pypi.org/project/autopep8/0.8/).  It is excellent;
I do not worry about these kinds of things until the end of a project.

