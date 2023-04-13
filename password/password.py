import sys
import string
import random
import json

query = sys.argv[1]

def create_item(title, subtitle, icon, arg):
    item = {}
    item['title'] = title
    item['subtitle'] = subtitle
    item['icon'] = icon
    item['arg'] = arg
    return item

items = []

try:
    length = int(query)
    if length <= 0:
        raise ValueError
    random_string = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))
    items.append(create_item(random_string, '生成后的密码', {'type': 'default', 'path': 'icon.png'},random_string))
except ValueError:
    items.append(create_item('Invalid input', 'Please enter a positive integer', {'type': 'default', 'path': 'icon.png'},''))

result = {}
result['items'] = items

print(json.dumps(result))
