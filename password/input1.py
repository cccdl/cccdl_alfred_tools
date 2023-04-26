import sys
import random
import string
import json


def generateSimplePassword(input1):
    """生成简单密码"""
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(input1))


def generateComplexPassword(input1):
    """生成复杂密码"""
    letters = string.ascii_letters
    digits = string.digits
    symbols = "!@#$%^&*()_+-="
    password = [random.choice(letters), random.choice(digits), random.choice(symbols)]
    password += [random.choice(letters + digits + symbols) for i in range(input1)]
    random.shuffle(password)
    return ''.join(password)


def main():
    """主函数"""
    input1 = sys.argv[1]
    # 转换input1为整数
    input1 = int(input1)
    simplePassword = generateSimplePassword(input1)
    complexPassword = generateComplexPassword(input1)
    result = {
        "items": [
            {
                "title": f"{simplePassword}",
                "subtitle": "【简单密码】按Cmd+C或回车将其复制到剪贴板",
                "arg": simplePassword,
                "mods": {
                    "cmd": {
                        "subtitle": "按Cmd+C或回车将其复制到剪贴板",
                        "arg": simplePassword,
                        "valid": True,
                        "icon": {
                            "path": "public.copied"
                        }
                    }
                }
            },
            {
                "title": f" {complexPassword}",
                "subtitle": "【复杂密码】按Cmd+C或回车将其复制到剪贴板",
                "arg": complexPassword,
                "mods": {
                    "cmd": {
                        "subtitle": "按Cmd+C或回车将其复制到剪贴板",
                        "arg": complexPassword,
                        "valid": True,
                        "icon": {
                            "path": "public.copied"
                        }
                    }
                }
            }
        ]
    }
    print(json.dumps(result))


if __name__ == '__main__':
    main()
