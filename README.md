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

`--no-dups` Use this one if you want to avoid having any of the words in
your input phrase in the list of anagrams at the end.

`--none-of` Use this to point to a file of words to exclude from the 
resulting anagrams. It is a better idea to build a special dictionary if
this is a list of words you plan to use regularly.

`--min-len` This tells the anagrammar the shortest word to consider. 

`--dictionary` In this project, I have provided two dictionaries already
compiled, but you can compile your own. The one named `mit10000` is built
from the 10,000 most common words in English. The one named `words` is much
larger, coming from the New Webster's Dictionary that is included with 
Linux in `/usr/share/dict/words`. Each dictionary is a pair of files.

`--cpu` The program can be caused to stop after a given number of seconds
of execution. I put this in when I was developing the program, and I never got
around to removing it.

`--verbose` This produces a running narrative to the screen to give you
the illusion that the program is making progress. 

### Start with something small.

How about *git hub is great* as the phrase? First, source the `anagram.bash` 
file, and you will then be able to just type `anagram` to run the program. The 
output will appear on the screen, which is not always useful if there are a lot
of anagrams to your phrase. In the example below, I directed the output to `x.out`.

```bash
anagram --dictionary mit10000 --min-len 3 "git hub is great" >x.out

 --cpu 0 --dictionary mit10000 --min-len 3 --no-dups False --phrase ['git', 'hub', 'is', 'great'] --verbose True

Initial pruning: 185 keys representing 238 words.

 D | branch |  dead  |  user  |  sys   |  page  |  I/O  | WAIT | USEDQ |  Tails  |
   | evals  |  ends  |  secs  |  secs  | faults |  sig  |  sig |       |         |
---+--------+--------+--------+--------+--------+-------+------+-------+---------|
  1    12890     2503     0.51     0.02     5588      70    172    127      1674

12890 branches in the tree. 2503 dead ends. Max depth 4.

real    0m0.588s
user    0m0.519s
sys     0m0.028s
```

`x.out` will contain a printed tree in which each path from the
root node to a leaf is an anagram of the target phrase, `git hub is great`.

Here is what the output file looks like:

```
Loading dictionaries.
Dictionaries loaded.
{   'bath': {'gig': {'tri': ('use', 'sue'), 'uri': ('est', 'ste', 'set')}},
    'beth': {'gig': {'tri': ('usa', 'aus')}},
    'bigger': {'utah': ('ist', 'its', 'sit'), ('shut', 'thus'): 'ati'},
    'biggest': {'hat': 'uri', ('air', 'ira'): 'thu'},
    'birth': {'suit': 'gage'},
    'bright': {'suit': 'age'},
    'butt': {'gage': 'irish'},
    'eight': {'suit': 'grab'},
    'gate': {'gui': {'bit': 'hrs'}},
    'gather': {'bits': 'gui'},
    'gratis': {'huge': 'bit'},
    'gratuit': {'big': 'she'},
    'guitar': {'beth': ('sig', 'gis')},
    'guitars': {'big': 'the'},
    'hair': {   'get': {('sig', 'gis'): ('tub', 'but')},
                'gst': {'big': 'tue', 'bug': 'tie', 'gui': 'bet'}},
    'hats': {'gui': {'bit': 'reg'}},
    'her': {'big': {'gui': 'stat'}},
    'hub': {   'gig': {('air', 'ira'): 'test', ('era', 'are', 'ear'): 'tits'},
               'tit': {('air', 'ira'): 'eggs'},
               ('ist', 'its', 'sit'): {'ati': 'greg'}},
    'huge': {('ist', 'its', 'sit'): {'big': ('rat', 'tar', 'art')}},
    'irish': {'gage': 'butt'},
    'itsa': {'egg': {'tri': 'hub'}},
    'rights': {'bite': 'aug'},
    'suite': {'right': ('bag', 'gba')},
    'tags': {'gui': {'bit': 'her'}},
    'that': {'big': {'gui': ('ser', 'res'), 'sie': 'rug'}, ('sig', 'gis'): {'big': 'eur'}},
    'tiger': {'sight': 'abu', 'thai': 'bugs'},
    'tigers': {'thai': 'bug'},
    'tight': {'urge': 'bias'},
    'true': {'big': {'tag': 'his'}},
    'urge': {'hit': {'big': 'sat'}, 'tit': {'big': ('has', 'ash')}},
    ('beat', 'beta'): {   'gig': {'hit': ('sur', 'usr'), 'thu': ('irs', 'sir', 'sri')},
                          ('sig', 'gis'): {'rug': 'hit'}},
    ('heat', 'hate'): {'big': {'gui': 'str', 'uri': 'gst'}, 'gig': {'tri': ('usb', 'sub', 'bus')}},
    ('sage', 'ages', 'sega'): {'hit': {'bug': 'tri'}},
    ('sig', 'gis'): {'big': {'eur': 'that'}},
    ('this', 'shit', 'hits', 'hist'): {   'big': {'tue': 'arg'},
                                          'gig': {('tub', 'but'): ('era', 'are', 'ear')},
                                          'gui': {'get': ('bar', 'bra')}},
    ('thru', 'hurt', 'ruth'): {   'big': {'isa': 'get', 'sie': 'tag', 'tie': 'gas'},
                                  'gig': {'bit': 'sea', 'sie': ('bat', 'tba', 'tab'), 'tie': 'abs'},
                                  ('sig', 'gis'): {'big': ('eat', 'ate', 'tea')}}}
```

I think "GUI tags bit her" is perhaps the best of the lot.

## Trivia Q & A.

### I don't like your dictionaries. How do I build one of my own?

The assumption in `dictbuilder.py` is that the input is a file of words, white
space delimited. You type in something like:

`python3 dictbuilder.py /path/to/your/file nameyouwanttouse`

The result will be two files, `nameyouwanttouse.forward` and `nameyouwanttouse.reversed`. 

### The PDF documentation looks like it is not finished.

Yes.

### Why did you put those operators in the CountedWord class?

I wrote C++ for 20 years before I switched to Python in 2014 and
regained my sanity. I experienced a flashback. It's like LSD, but worse.

### Why do you have operators you in the CountedWord class that you don't use?

I know they are there. Time will tell whether they become
useful. There are loose ends.

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

