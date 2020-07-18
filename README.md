# anagrammar
A brute force anagram finder, teaching tool, and a one gram pun. For more 
information, please consult [Lisa Simpson](https://www.youtube.com/watch?v=cj71HnSJaUM).

## Why did you write this program?

Because programming in Python should be fun.

### Curiosity

A number of people with whom I work use the 
[Internet Anagram Server](https://new.wordsmith.org/anagram/), 
and we are not alone. It seems always to be down, or overwhelmed by
requests. To minimize its CPU usage, it works with a small list of 
common words. I'm interested in fewer, longer words.

For example, `embrace inclusivity` is an anagram for 

- `unmiscable veracity`
- `cystic nerve bulimia`

and several other phrases.

### Python programming

Many teaching examples are not all that useful for improving one's 
programming. They are minimum working examples of .. something ..,
but programming is not best learned in MWE size bites, just as human
language is not learned one word at a time. If you studied Spanish and
learned that "me | gusta | la | pitón" is "to me | is pleasing | the | python," you are
never going to learn Spanish. Give up now.

This one-file program covers several different data structures, all of which
are built into Python. Using them is an important part of Python programming:

- `collections.Counter`
- derived `class` from `collections.Counter`
- `collections.defaultdict`
- exploitation of the Python object model.
- `argparse`

The file is a good demonstration of how much you can get done with very little Python:

```
-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
Python                           1             32             46             98
-------------------------------------------------------------------------------
```

## What do you need to run it?

1. A standard distro of Python.
2. Some lists of words that make up the allowable words to use in the anagram. If you run the program on
Linux or Mac OS, the program should find the system dictionaries without your having to do anything 
extra. Windows is a BYODictionary experience. 

## Your code is shit. Why did you ...?

OK, first I have heard worse, and I have committed bigger sins. A friend once described my 
programming as "entirely adequate." A written performance review once included the
words "the only thing George knows how to do is write a compiler." I suppose each statement
is still true.

#### ... not follow PEP-8 exactly?

If it bothers you, you can experiment with [AutoPEP8](https://pypi.org/project/autopep8/0.8/).
It is excellent; I am just lazy.

#### ... leave a bug on line XXXX?

Wow. Well spotted. You can email me at me+anagrammar@georgeflanagin.com, or just fork it and fix it.

#### ... mix f-strings and format() statements?

I wrote this in 2 1/2 hours while drinking bourbon and despairing over the state of the country. I cannot recall if it was 
[Ragged Branch](https://www.raggedbranch.com) or 
[Isaac Bowman](https://asmithbowman.com/isaac-bowman/). This code is recreation. It is a distraction from the more serious woes.

#### ... put those operators in the Bag class?

I wrote C++ for years before I switched to Python in 2014 and regained my sanity. I experienced a flashback.

#### ... have operators you in the Bag class that you don't use?

Yes, I know they are there. Time will tell whether they become useful. I needed to get some sleep, so there are a few loose ends.

#### ... have unimplemented command line options?

Yes, I know. Chill out. Python should be fun. 

