import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

qyery = base64.b64decode(b'xF09ZQKbxCDkiiSZUWclvA==')

print(qyery)

key = b'nAdYRsCATiFMXfEr'
cipher = AES.new(key, AES.MODE_ECB)
a = cipher.decrypt(qyery)

str = unpad(a, 16)
print(str.decode())

