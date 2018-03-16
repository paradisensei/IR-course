# -*- coding: utf-8 -*-

import io, json
from sys import argv
from string import punctuation

# fetch required index type from command line arguments
if len(argv) != 2 or argv[1] not in ('porter', 'mystem'):
    raise ValueError("Pass index type (porter/mystem) to the script")
else:
    type = argv[1]

index = {}

articles = json.load(open('../task2/result.json'))['articles']

def remove_punctuation(s):
    return ''.join(c for c in s if c not in punctuation)

# iterate over all articles & construct index
for a in articles:
    # remove punctuation from title & abstract
    title = remove_punctuation(a['title'][type])
    abstract = remove_punctuation(a['abstract'][type])
    # construct doc by joining terms in title & abstract
    doc = title.split() + abstract.split()
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
    index[term]['count'] = len(index[term]['docs'])

# save results to JSON file
def set_default(obj):
    if isinstance(obj, set):
        return sorted(list(obj))
    return obj

with io.open(type + '_index.json', 'w', encoding='utf-8') as out:
    out.write(json.dumps(index, indent=2, ensure_ascii=False, default=set_default))
