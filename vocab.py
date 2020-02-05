#!/usr/bin/env python3.7

import requests
import re


PATTERN_CATEGORY = re.compile(r'href="(.*?)">(.*?)<')
PATTERN_SUBLIST = re.compile(r'<a href="(.*?)">(.*?)</a>')
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
        categories[m.group(2).strip()] = {'path': m.group(1)[len(BASE_URL):]}
    global CATEGORIES
    CATEGORIES = categories
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
        m = PATTERN_CATEGORY.finditer(r.text[pos:p2]).__next__()
        c = m.group(2).strip()
        topics[c] = {'path': m.group(1)[len(BASE_URL):], 'sublists': {}}
        for m in PATTERN_SUBLIST.finditer(r.text[pos:p2 + 10]):
            topics[c]['sublists'][m.group(2).strip()] = {'path': m.group(1)}
    return topics


if __name__ == '__main__':
    get_categories()
    for name, url in CATEGORIES.items():
        print(name)
        t = get_topics(name)
        for n, u in t.items():
            print(f'  {n}')
            for n2, u2 in u['sublists'].items():
                print(f'    {n2}')
