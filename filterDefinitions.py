import re as re

index = 'terrorism'
file = 'in/war_and_conflict.html'

out = file + '-' + index + '.csv'
#pattern = '\"/definition/english/.*?\">.*?<'
pattern = 'data-' + index + '_t=\"..\">..<a href=\"/definition/english/.*?\">.*?<'


def find():
    re.compile(pattern)
    with open(file) as f:
        content = f.read()
        return re.findall(pattern, content)


def compute(definitions):
    lists = []
    for definition in definitions:
        text = definition[definition.rindex('>') + 1: definition.rindex('<')]
        lists.append(text)
    return lists


def delete_duplicates(definitions):
    return list(dict.fromkeys(definitions))


def write_to_file(name, definitions):
    with open(name, 'w+') as f:
        f.write(';\n'.join(definitions))


vocabs = find()
vocabs = compute(vocabs)
vocabs = delete_duplicates(vocabs)
write_to_file(out, vocabs)
print(vocabs)







