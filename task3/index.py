# -*- coding: utf-8 -*-

import io, json
from sys import argv
from math import log

# fetch required index type from command line arguments
if len(argv) != 2 or argv[1] not in ('porter', 'mystem'):
    raise ValueError("Pass index type (porter/mystem) to the script")
else:
    type = argv[1]

index = {}

articles = json.load(open('../task2/result.json'))['articles']

# iterate over all articles & construct index
for a in articles:
    # construct doc by joining terms in title & abstract
    doc = a['title'][type].split() + a['abstract'][type].split()
    doc_id = a['url']
    # iterate over terms and update index step by step
    for term in doc:
        if term in index:
            index[term]['docs'].add(doc_id)
        else:
            index[term] = {
                'docs': {doc_id}
            }

# iterate over index and add docs count
for term in index:
    count = len(index[term]['docs'])
    index[term]['count'] = count
    index[term]['idf'] = log(len(articles) / count, 2)

# save results to JSON file
def set_default(obj):
    if isinstance(obj, set):
        return sorted(list(obj))
    return obj

with io.open(type + '_index.json', 'w', encoding='utf-8') as out:
    out.write(json.dumps(index, indent=2, ensure_ascii=False, default=set_default))
