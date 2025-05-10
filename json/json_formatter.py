import sys
import json
import subprocess
import os

def main():
    if len(sys.argv) < 2 or not sys.argv[1].strip():
        print("请输入JSON字符串")
        return

    input_str = sys.argv[1]
    json_line = next((line for line in input_str.strip().split('\n') if line.strip()), None)
    if not json_line:
        print("未检测到有效JSON行")
        return

    try:
        obj = json.loads(json_line)
        pretty = json.dumps(obj, ensure_ascii=False, indent=4)
        # 复制到剪贴板
        subprocess.run('pbcopy', input=pretty.encode('utf-8'))
        # 写入指定目录
        temp_path = '/Users/long/Downloads/json_formatter_temp.json'
        with open(temp_path, 'w', encoding='utf-8') as f:
            f.write(pretty)
        # 用 Chrome 打开
        subprocess.run(['open', '-a', 'Google Chrome', temp_path])
        print(f"已复制到剪贴板，并在Chrome中打开格式化后的JSON，文件路径: {temp_path}")
    except Exception as e:
        print("JSON解析失败：", str(e))

if __name__ == '__main__':
    main() 