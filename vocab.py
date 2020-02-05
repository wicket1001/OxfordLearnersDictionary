#!/usr/bin/env python3.7

import requests
import re


PATTERN_TOPIC = re.compile(r'href="(.*?)">(.*?)<')
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
        m = PATTERN_TOPIC.finditer(r.text[pos:pos+200]).__next__()
        categories[m.group(2)] = {'path': m.group(1)[len(BASE_URL):]}
    global CATEGORIES
    CATEGORIES = categories
    return categories


def get_topics(category):
    r = requests.get(f'{BASE_URL}{CATEGORIES[category]["path"]}')
    pos = 0
    topics = {}
    while True:
        pos = r.text.find('topic-box-secondary-heading', pos + 1)
        if pos == -1:
            break
        m = PATTERN_TOPIC.finditer(r.text[pos:pos+200]).__next__()
        topics[m.group(2)] = {'path': m.group(1)[len(BASE_URL):]}
    return topics


if __name__ == '__main__':
    get_categories()
    for name, url in CATEGORIES.items():
        print(name)
        t = get_topics(name)
        for n, u in t.items():
            print(f'  {n}')
