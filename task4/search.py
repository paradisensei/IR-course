# -*- coding: utf-8 -*-

import io, json
from sys import argv

# fetch required index type and terms from command line arguments
if len(argv) < 3 or argv[1] not in ('porter', 'mystem'):
    raise ValueError("Pass index type (porter/mystem) and terms to the script")
else:
    type = argv[1]
    terms = map(lambda t: t.decode('utf-8'), argv[2:])

# load the right index
index = json.load(open('../task3/' + type + '_index.json'))

"""
Searches the intersection & exclusion of corresponding docs
"""
def search(index, terms):
    include = set()
    exclude = set()
    for t in terms:
        exl = t.startswith('-')
        if exl and t[1:] not in index or not exl and t not in index:
            continue
        if exl:
            exclude |= set(index[t[1:]]['docs'])
        else:
            include |= set(index[t]['docs'])
    return list(include - exclude)

docs = search(index, terms)
for doc in docs:
    print doc