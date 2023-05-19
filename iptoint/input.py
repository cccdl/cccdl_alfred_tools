import sys
import socket
import struct
import json


def ip_to_int(ip_address):
    packed_ip = socket.inet_aton(ip_address)
    return struct.unpack('!I', packed_ip)[0]


def main():
    """主函数"""
    input1 = sys.argv[1]
    ipInteger = ip_to_int(input1)
    result = {
        "items": [
            {
                "title": f"{ipInteger}",
                "subtitle": "【ip转int】按Cmd+C或回车将其复制到剪贴板",
                "arg": ipInteger,
                "mods": {
                    "cmd": {
                        "subtitle": "按Cmd+C或回车将其复制到剪贴板",
                        "arg": ipInteger,
                        "valid": True,
                        "icon": {
                            "path": "public.copied"
                        }
                    }
                }
            },
        ]
    }
    print(json.dumps(result))


if __name__ == '__main__':
    main()
