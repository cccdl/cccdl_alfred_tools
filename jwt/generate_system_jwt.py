#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import base64
import hmac
import hashlib
import time
from datetime import datetime, timedelta

# --- 辅助函数：用于JWT令牌生成 ---
def base64url_encode(data):
    """执行Base64URL编码，用于JWT令牌的头部和负载部分"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    # 标准base64编码
    encoded = base64.b64encode(data).decode('utf-8')
    
    # 转换为base64url格式
    return encoded.replace('+', '-').replace('/', '_').rstrip('=')

def validate_inputs(access_secret, user_id):
    """验证输入参数是否有效"""
    if not access_secret:
        raise ValueError("accessSecret不能为空")
    if not user_id:
        raise ValueError("userId不能为空")
    return True

def generate_system_jwt(access_secret, user_id):
    """
    生成系统级别的JWT令牌，用于定时任务等系统操作
    
    参数:
        access_secret: 签名密钥
        user_id: 用户ID
        
    返回:
        str: 生成的JWT令牌
    """
    # 验证输入参数
    validate_inputs(access_secret, user_id)
    
    # 创建JWT头部
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }
    
    # 创建JWT负载
    now = int(time.time())
    expiry = now + (30 * 24 * 60 * 60)  # 30天有效期
    
    payload = {
        "exp": expiry,
        "iat": now,
        "userId": user_id
    }
    
    # 编码头部和负载
    header_encoded = base64url_encode(json.dumps(header))
    payload_encoded = base64url_encode(json.dumps(payload))
    
    # 创建签名信息
    message = f"{header_encoded}.{payload_encoded}"
    signature = hmac.new(
        access_secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).digest()
    
    # 编码签名
    signature_encoded = base64url_encode(signature)
    
    # 组装JWT
    token = f"{message}.{signature_encoded}"
    
    return token

def parse_input_from_alfred():
    """
    从Alfred传入的参数 (sys.argv) 中解析accessSecret和userId
    
    返回:
        tuple: (access_secret, user_id)
    """
    try:
        # 从 sys.argv 获取用户输入
        # sys.argv[0] 是脚本名, sys.argv[1] 应该是Alfred传入的 {query}
        if len(sys.argv) > 1:
            input_str = sys.argv[1]
        else:
            # 没有足够的参数传入
            return '', ''
        
        if not input_str.strip(): # 检查输入是否为空或仅包含空格
            return '', ''
        
        # 先检查是否是JSON格式 (适用于某些Alfred版本)
        try:
            data = json.loads(input_str)
            if isinstance(data, dict):
                return data.get('key', ''), data.get('user', 'system_user')
        except json.JSONDecodeError:
            pass
        
        # 处理空格分隔的参数
        parts = input_str.split()
        
        # Alfred脚本过滤器的各种可能情况
        if len(parts) >= 3 and parts[0].lower() in ["jwt", "generate"]:
            # 例如: "jwt 密钥 用户ID"
            return parts[1], parts[2]
        elif len(parts) >= 2:
            # 例如: "密钥 用户ID"
            return parts[0], parts[1]
        elif len(parts) == 1:
            # 只有密钥，使用默认用户ID
            return parts[0], "system_user"
    except Exception:
        # 静默处理异常，返回空值
        pass
    
    return '', ''

def main():
    """主函数：处理输入、生成JWT并返回结果"""
    try:
        # 解析输入参数
        access_secret, user_id = parse_input_from_alfred()
        
        if not access_secret or not user_id:
            # 返回错误信息，符合Alfred脚本过滤器格式
            error_result = {
                "items": [
                    {
                        "title": "请输入密钥",
                        "subtitle": "格式: 你的密钥 [用户ID]",
                        "arg": "error",
                        "valid": False
                    }
                ],
                "variables": {
                    "error": "请按正确格式输入参数",
                    "status": "error"
                }
            }
            print(json.dumps(error_result))
            return
        
        # 生成JWT令牌
        token = generate_system_jwt(access_secret, user_id)
        
        # 计算过期时间，便于显示
        now = datetime.now()
        expiry_date = now + timedelta(days=30)
        expiry_formatted = expiry_date.strftime("%Y-%m-%d %H:%M:%S")
        
        # 输出结果，符合Alfred 5脚本过滤器JSON格式
        result = {
            "items": [
                {
                    "title": "JWT令牌已生成",
                    "subtitle": token,
                    "arg": token,
                    "valid": True,
                    "mods": {
                        "cmd": {
                            "subtitle": "⌘: 复制完整令牌到剪贴板"
                        },
                        "alt": {
                            "subtitle": "⌥: 查看令牌详情"
                        }
                    },
                    "text": {
                        "copy": token,
                        "largetype": token
                    }
                }
            ],
            "variables": {
                "token": token,
                "expiry_date": expiry_formatted,
                "expires_in": "30天",
                "user_id": user_id,
                "status": "success"
            }
        }
        
        print(json.dumps(result))
        
    except Exception as e:
        # 输出错误信息，符合Alfred脚本过滤器格式
        error_message = str(e)
        error_result = {
            "items": [
                {
                    "title": "JWT生成失败",
                    "subtitle": error_message,
                    "arg": "error",
                    "valid": False
                }
            ],
            "variables": {
                "error": error_message,
                "status": "error"
            }
        }
        print(json.dumps(error_result))

if __name__ == "__main__":
    main()
