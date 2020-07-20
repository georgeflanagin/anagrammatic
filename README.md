# anagrammar

A brute force anagram finder, teaching tool, and a one gram pun.
For more information, please consult [Lisa
Simpson](https://www.youtube.com/watch?v=cj71HnSJaUM).

## Why did you write this program?

Because programming in Python should be fun. I frequently need
teaching examples, and this seems like a good one: the topic is
simple and familiar, with the implementation revealing some design
choices and difficulties.

A number of people with whom I work use the [Internet Anagram
Server](https://new.wordsmith.org/anagram/), and we are not alone.
It seems always to be down, or overwhelmed by requests. To minimize
its CPU usage, it works with a small list of common words. I'm
interested in fewer, longer words.

For example, `embrace inclusivity` is an anagram for 

- `unmiscable veracity`
- `cystic nerve bulimia`

and a few other phrases.

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

```bash
python anagrammar.py --dictionary words --min-len 3 githubisgreat >x.out

Initial pruning: 493 keys representing 789 words.

  tree | user |  sys | faults |  I/O  | WAIT | USEDQ|
------------------------------------------------------------
   5100   2.18   0.05   32675       0      3    319

5117 keys tried.
```

At the end of these 2.18+ seconds, `x.out` will contain a printed
tree in which each path from the root node to a leaf is an anagram
of the target phrase, `githubisgreat`. In the example, there are
230. Words that are self-anagrams, like `('thus', 'shut', 'tush')` 
are shown in parentheses.

### Trivia Q & A.

#### Why did you put those operators in the CountedWord class?

I wrote C++ for years before I switched to Python in 2014 and
regained my sanity. I experienced a flashback.

#### Why do you have operators you in the CountedWord class that you don't use?

Yes, I know they are there. Time will tell whether they become
useful. There are loose ends.

#### Why are the dictionaries saved as pickles? That limits their use to Python. 

This is why God gave you the ability to fork the repo. The dictionaries are
built and read entirely within the file `dictbuilder.py`, so you can change
this. There are only about 100 lines of code that do the work. 

#### Why did you not follow PEP-8 exactly? Your style is terrible. 

OK, first I have heard worse and I have committed bigger sins. My best 
professional friend once described my programming as "entirely adequate." A
written performance review once included the words "the only thing
George knows how to do is write a compiler."

If it bothers you, you can experiment with
[AutoPEP8](https://pypi.org/project/autopep8/0.8/).  It is excellent;
I do not worry about these kinds of things until the end of a project.

