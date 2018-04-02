import io, json
from sys import argv

from lsi import LSI

# fetch required articles type and query from command line arguments
if len(argv) < 3 or argv[1] not in ('porter', 'mystem'):
    raise ValueError("Pass articles type (porter/mystem) and query to the script")
else:
    type = argv[1]
    query = ' '.join(map(lambda t: t.decode('utf-8'), argv[2:]))

# load articles and construct docs array
articles = json.load(open('../task2/result.json'))['articles']
docs = [' '.join([a['title'][type], a['abstract'][type]]) for a in articles]

# rank
lsi = LSI(docs, query)
ranking = lsi.process()
print ranking