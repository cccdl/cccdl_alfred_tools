import sys
import string
import random
import json

query = sys.argv[1]


def createItem(title, subtitle, icon, arg):
    item = {'title': title, 'subtitle': subtitle, 'icon': icon, 'arg': arg}
    return item


items = []

try:
    length = int(query)
    if length <= 0:
        raise ValueError
    randomString = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))
    items.append(createItem(randomString, '生成后的密码', {'type': 'default', 'path': 'icon.png'}, randomString))
except ValueError:
    items.append(
        createItem('Invalid input', 'Please enter a positive integer', {'type': 'default', 'path': 'icon.png'}, ''))

result = {'items': items}

print(json.dumps(result))
