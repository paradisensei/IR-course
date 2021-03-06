# -*- coding: utf-8 -*-

from __future__ import division

import io, json
from sys import argv
from collections import Counter

# fetch required index type and query from command line arguments
if len(argv) < 3 or argv[1] not in ('porter', 'mystem'):
    raise ValueError("Pass index type (porter/mystem) and query to the script")
else:
    type = argv[1]
    terms = map(lambda t: t.decode('utf-8'), argv[2:])

# load the right index
index = json.load(open('../task3/' + type + '_index.json'))
# load articles info
articles = json.load(open('../task2/result.json'))['articles']

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

doc_ids = search(index, terms)

doc_score = {}

for doc_id in doc_ids:
    doc = next(
        a['title'][type].split() + a['abstract'][type].split() 
        for a in articles if a['url'] == doc_id
    )
    count = len(doc)
    term_count = Counter(doc)
    
    score = 0
    for t in terms:
        if not t.startswith('-'):
            tf = term_count[t] / count
            score += tf * index[t]['idf']
    doc_score[doc_id] = score

doc_score = sorted(doc_score.items(), key=lambda x: x[1], reverse=True)

query = ' '.join(terms)
result = {
    query: []
}

for doc, score in doc_score:
    result[query].append({
        doc: score
    })

# save results to JSON file
with io.open('result1.json', 'w', encoding='utf-8') as out:
    out.write(json.dumps(result, indent=2, ensure_ascii=False))