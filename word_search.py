#!/usr/bin/env python3

def possible_words(terms,allowed):
    terms = terms.split(" ") if isinstance(terms,str) else terms
    allowed = set(allowed) if isinstance(allowed,str) else allowed
    a = len(allowed)
    for t in terms:
        l = set(t)
        if len(l) > a:
            continue
        if len(l - allowed) < 1:
            yield t

from sys import argv
terms = "cat dog hog movie"
allowed = "dog" if len(argv) < 2 else " ".join(argv[1:])
try: terms = filter(len,map(str.strip,open("data/terms.txt","r")))
except: pass

print(*list(possible_words(terms,allowed)),sep='\n')
