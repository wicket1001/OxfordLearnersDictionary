#!/usr/bin/env python3.7

import requests
import re


PATTERN_CATEGORY = re.compile(r'href="(.*?)">(.*?)<')
PATTERN_SUBLIST = re.compile(r'<a href="(.*?)">(.*?)</a>')
PATTERN_VOCAB = re.compile(r'<li id="(.*?)" data-hw="(.*?)" data-(.*?)_t="(.*?)">\s*<a href="(.*?)">(.*?)</a><span class="pos">(.*?)</span><div><span class="belong-to">(.*)</span>')
BASE_URL = 'https://www.oxfordlearnersdictionaries.com'
LINK_TOPIC = '/topic/'

CATEGORIES = {}


def get_categories():
    r = requests.get(f'{BASE_URL}{LINK_TOPIC}')
    pos = 0
    categories = {}
    while True:
        pos = r.text.find('topic-label', pos + 1)
        if pos == -1:
            break
        m = PATTERN_CATEGORY.finditer(r.text[pos:pos+200]).__next__()
        categories[m.group(2).strip()] = {'path': m.group(1)[len(BASE_URL):], 'topics': {}}
    global CATEGORIES
    CATEGORIES = categories
    for name, obj in CATEGORIES.items():
        get_topics(name)
    return categories


def get_topics(category):
    r = requests.get(f'{BASE_URL}{CATEGORIES[category]["path"]}')
    pos = 0
    topics = {}
    while True:
        pos = r.text.find('topic-box-secondary-heading', pos + 1)
        p2 = r.text.find('</a>\n                                    </div>', pos)
        if pos == -1:
            break
        m = PATTERN_CATEGORY.findall(r.text[pos:p2])[0]
        c = m[1].strip()
        topics[c] = {'title': m[1].strip(), 'path': m[0][len(BASE_URL):], 'sublists': {}}
        for m in PATTERN_SUBLIST.finditer(r.text[pos:p2 + 10]):
            sl = m.group(1)[len(BASE_URL):]
            sl = sl[sl.find('=') + 1:sl.rfind('_')]
            topics[c]['sublists'][sl] = {'title': m.group(2).strip(), 'path': m.group(1)[len(BASE_URL):], 'vocabs': []}
    CATEGORIES[category]['topics'] = topics
    for name, obj in CATEGORIES[category]['topics'].items():
        get_vocabs(category, name)
    return topics


def get_vocabs(category, topic):
    r = requests.get(f'{BASE_URL}{CATEGORIES[category]["topics"][topic]["path"]}')
    p1 = r.text.find('top-g')
    p2 = r.text.find('</ul>', p1)
    t = r.text[p1:p2]
    lpos = 0
    pos = 0
    while True:
        pos = t.find('</li>', pos + 1)
        if pos == -1:
            break
        m = PATTERN_VOCAB.findall(t[lpos:pos])[0]
        CATEGORIES[category]['topics'][topic]['sublists'][m[2]]['vocabs'].append({
            'vocab': m[5],
            'type': m[6],
            'definitionLink': m[4],
            'definition': get_definition(m[4], category),
            'level': m[6]
        })
        lpos = pos


def get_definition(link, category):
    r = requests.get(f'{BASE_URL}{link}')
    p1 = r.text.find('<ol')
    p2 = r.text.find('</ol>', p1)
    t = r.text[p1:p2]
    lpos = 0
    pos = 0
    while True:
        pos = t.find('<li class="sense"', pos + 1)
        li = t[lpos:pos]
        pt1 = li.find('topic_name')
        if pt1 != -1:
            pt1 = li.find('>', pt1)
            pt2 = li.find('<', pt1)
            cat = li[pt1 + 1:pt2].strip()
            if cat == category:
                pd1 = li.find('class="def"')
                pd1 = li.find('>', pd1)
                pd2 = li.find('</span></span>', pd1)
                #print(li)
                definition = li[pd1 + 1:pd2].strip()
                #definition = re.sub(r'<.*?>', '', definition)
                print(definition)
        if pos == -1:
            break
        lpos = pos
    return None


if __name__ == '__main__':
    get_categories()
    for cat_name, cat in CATEGORIES.items():
        print(f'{cat_name}:')
        for topic_name, topic in cat['topics'].items():
            print(f'  {topic_name}:')
            for sl_name, sl in topic['sublists'].items():
                print(f'    {sl["title"]}:')
                for vocab in sl['vocabs']:
                    print(f'      {vocab["vocab"]}')

