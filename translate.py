import requests

filename = 'in/war_and_conflict.html-terrorism.csv'

BASE_URL = 'https://www.deepl.com/translator#en/de/'


if __name__ == '__main__':
    with open(f'{filename}') as f:
        r = requests.get(f'{BASE_URL}{f.read()}')
        print(r.text)







