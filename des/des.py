import base64
import sys
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def createItem(title, subtitle, icon, arg):
    item = {'title': title, 'subtitle': subtitle, 'icon': icon, 'arg': arg}
    return item


a = sys.argv[1]
str = a.encode()
qyery = base64.b64decode(str)

key = b'nAdYRsCATiFMXfEr'
cipher = AES.new(key, AES.MODE_ECB)
a = cipher.decrypt(qyery)

str = unpad(a, 16)
b = str.decode()

items = []

items.append(createItem(b, '结果', {'type': 'default', 'path': 'icon.png'}, b))

result = {'items': items}

print(json.dumps(result))
