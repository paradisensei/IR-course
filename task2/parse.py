# -*- coding: utf-8 -*-

import io, json
import requests
from lxml import html
from string import punctuation

# porter stemming algorithm
from porter import Porter
# Yandex Mystem 3.0 wrapper (pip install pymystem3)
from pymystem3 import Mystem
m = Mystem()

# constants
base_url = 'http://www.mathnet.ru'
search_url = base_url + '/php/archive.phtml?jrnid=ivm&wshow=issue&year=2017&volume=&volume_alt=&issue=2&issue_alt=&option_lang=rus'

result = {
    'issue': search_url,
    'articles': []
}

# get html page
tree = html.fromstring(requests.get(search_url).content)

# get <a> tags with links to articles
articles = filter(
    lambda a: a.get('href').startswith('/rus'),
    tree.xpath("//a[contains(@class,'SLink')]")
)

def remove_punctuation(s):
    return ''.join(c for c in s if c not in punctuation)

# iterate over all articles & retrieve necessary data
for a in articles:
    url = base_url + a.get('href')
    article = html.fromstring(requests.get(url).content)

    title = a.text
    title_clear = remove_punctuation(title)
    title_porter = ' '.join(map(Porter.stem, title_clear.split()));
    title_mystem = ''.join(m.lemmatize(title_clear)).strip()
    
    abstract = article.xpath(u"//b[contains(text(), 'Аннотация')]/following-sibling::text()")[0].strip()
    abstract_clear = remove_punctuation(abstract)
    abstract_porter = ' '.join(map(Porter.stem, abstract_clear.split()));
    abstract_mystem = ''.join(m.lemmatize(abstract_clear)).strip()

    keywords = article.xpath(u"//b[contains(text(), 'Ключевые')]/following-sibling::i")[0].text[:-1].split(', ')
    result['articles'].append({
        'url': url,
        'title': {
            'original': title,
            'porter': title_porter,
            'mystem': title_mystem
        },
        'abstract': {
            'original': abstract,
            'porter': abstract_porter,
            'mystem': abstract_mystem
        },
        'keywords': keywords
    })

# save results to JSON file
with io.open('result.json', 'w', encoding='utf-8') as out:
    out.write(json.dumps(result,  indent=2, ensure_ascii=False))