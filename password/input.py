import json

item = []

item.append({
    'title': '简易密码',
    'subtitle': '',
    'arg': 1
})

item.append({
    'title': '复杂密码',
    'subtitle': '带特殊字符',
    'arg': 2
})

result = {'items': item}

print(json.dumps(result))

