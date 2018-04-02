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
    include = []
    exclude = set()
    for t in terms:
        exl = t.startswith('-')
        if exl and t[1:] not in index:
            continue
        if not exl and t not in index:
            include.append(set())
            continue
        if exl:
            exclude |= set(index[t[1:]]['docs'])
        else:
            include.append(set(index[t]['docs']))
    return list(set.intersection(*include) - exclude)

result = {
    ' '.join(terms): search(index, terms)
}

# save results to JSON file
with io.open('result1.json', 'w', encoding='utf-8') as out:
    out.write(json.dumps(result, indent=2, ensure_ascii=False))