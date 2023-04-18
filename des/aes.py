import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# 加密内容
str = '123456789'
data = str.encode()


print('转换bytes：')
print(data)
key = b'nAdYRsCATiFMXfEr'
cipher = AES.new(key, AES.MODE_ECB)
a = cipher.encrypt(pad(data, 16))
print('aes加密')
print(a)

print('base64加密：')
print(base64.b64encode(a))
