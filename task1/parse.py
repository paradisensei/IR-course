# -*- coding: utf-8 -*-

import io, json
import requests
from lxml import html

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

# iterate over all articles & retrieve necessary data
for a in articles:
    url = base_url + a.get('href')
    title = a.text
    article = html.fromstring(requests.get(url).content)
    abstract = ''.join(article.xpath(u"//b[contains(text(), 'Аннотация')]/following-sibling::text()[not(preceding-sibling::b[contains(text(), 'Ключевые')])]")).strip()
    keywords = article.xpath(u"//b[contains(text(), 'Ключевые')]/following-sibling::i")[0].text[:-1].split(', ')
    result['articles'].append({
        'url': url,
        'title': title,
        'abstract': abstract,
        'keywords': keywords
    })

# save results to JSON file
with io.open('result.json', 'w', encoding='utf-8') as out:
    out.write(json.dumps(result,  indent=2, ensure_ascii=False))