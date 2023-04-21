import json
import sys

item = []
a1 = {
    'title': '简易密码',
    'subtitle': '',
    'arg': 1
}
a2 = {
    'title': '复杂密码',
    'subtitle': '带特殊字符',
    'arg': 2
}
item.append(a1)

item.append(a2)

result = {'items': item}

if len(sys.argv) == 2:
    query = sys.argv[1]
    if query == '1':
        item.remove(a2)
    elif query == '2':
        item.remove(a1)

print(json.dumps(result))
