import json

item = []

item.append({
    'title': '不包含特殊字符的密码',
    'subtitle': '',
    'arg': 1
})

item.append({
    'title': '特殊字符的密码',
    'subtitle': '',
    'arg': 2
})

result = {'items': item}

print(json.dumps(result))
