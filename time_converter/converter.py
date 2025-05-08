import sys
import json
from datetime import datetime, timezone, timedelta
import re

try:
    import dateutil.parser
except ImportError:
    dateutil = None

# --- 辅助函数：用于解析和转换 ---
def is_timestamp_like(input_str):
    """检查输入是否像一个时间戳 (纯数字，可能带小数点)"""
    return re.fullmatch(r'^-?\d+(\.\d+)?$', input_str) is not None

def parse_input_to_datetime(input_str_from_arg):
    """
    解析从上一个脚本的 'arg' 传递过来的字符串，尝试将其转换为 datetime 对象。
    """
    input_str = input_str_from_arg.strip()

    if input_str.lower() == "now":
        return datetime.now() # 返回当前本地时间

    if is_timestamp_like(input_str):
        try:
            ts = float(input_str)
            # 简单判断秒或毫秒 (13位数字通常是毫秒级时间戳)
            if len(input_str.split('.')[0]) >= 13 and not '.' in input_str:
                ts /= 1000
            # datetime.fromtimestamp 假定输入是本地时区的时间戳
            return datetime.fromtimestamp(ts)
        except ValueError:
            # 如果转换失败，继续尝试其他格式
            pass 

    # 尝试多种常见的日期和日期时间格式
    # strptime 返回的是 naive datetime 对象，代表本地时间
    datetime_formats = [
        '%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M:%S', '%Y.%m.%d %H:%M:%S',
        '%Y-%m-%d %H:%M', '%Y/%m/%d %H:%M', '%Y.%m.%d %H:%M',
        '%Y-%m-%d', '%Y/%m/%d', '%Y.%m.%d',
        '%m/%d/%Y %H:%M:%S', '%m-%d-%Y %H:%M:%S',
        '%m/%d/%Y %H:%M', '%m-%d-%Y %H:%M',
        '%m/%d/%Y', '%m-%d-%Y'
    ]
    for fmt in datetime_formats:
        try:
            return datetime.strptime(input_str, fmt)
        except ValueError:
            continue
    
    # 如果所有解析都失败
    raise ValueError(f"无法解析输入: \"{input_str}\"")

def generate_time_formats_for_alfred(dt_obj_local):
    """
    接收一个本地时区的 datetime 对象，生成多种时间格式的 Alfred 项目列表。
    """
    # 确保我们有一个时区感知的本地时间对象，以便正确转换为UTC
    # 如果 dt_obj_local 是 naive, astimezone() 会赋予它当前系统的本地时区
    if dt_obj_local.tzinfo is None or dt_obj_local.tzinfo.utcoffset(dt_obj_local) is None:
        dt_obj_local = dt_obj_local.astimezone()

    dt_utc = dt_obj_local.astimezone(timezone.utc)
    dt_utc_plus_8 = dt_utc.astimezone(timezone(timedelta(hours=8)))

    formats_dict = {
        "时间戳 (秒)": int(dt_utc.timestamp()),
        "时间戳 (毫秒)": int(dt_utc.timestamp() * 1000),
        "本地时间 (当前系统时区)": dt_obj_local.strftime('%Y-%m-%d %H:%M:%S'),
        "本地日期 (当前系统时区)": dt_obj_local.strftime('%Y-%m-%d'),
        "中国标准时间 (UTC+8)": dt_utc_plus_8.strftime('%Y-%m-%d %H:%M:%S'),
        "中国标准日期 (UTC+8)": dt_utc_plus_8.strftime('%Y-%m-%d'),
        "UTC 标准时间": dt_utc.strftime('%Y-%m-%d %H:%M:%S UTC'),
        "UTC 标准日期": dt_utc.strftime('%Y-%m-%d (UTC)')
    }

    alfred_items = []
    for title_suffix, value in formats_dict.items():
        alfred_items.append({
            "title": str(value),
            "subtitle": title_suffix,
            "arg": str(value), # 'arg' 用于复制到剪贴板
            "valid": True
        })
    return alfred_items

# --- 主逻辑 --- 
def main():
    """
    Alfred Script: 接收从上一个脚本选定项的 'arg' (通过 sys.argv[1])。
    解析该 'arg'，执行时间转换，并输出 Alfred JSON 项目列表。
    """
    if len(sys.argv) < 2 or not sys.argv[1].strip():
        input1 = 'now'
    else:
        input1 = sys.argv[1]
    try:
        dt_utc = parse_time(input1)
        # 0时区时间
        utc_str = dt_utc.strftime("%Y-%m-%d %H:%M:%S")
        # 中国本地时间
        dt_cn = dt_utc.astimezone(timezone(timedelta(hours=8)))
        cn_str = dt_cn.strftime("%Y-%m-%d %H:%M:%S")
        # 时间戳（秒/毫秒）
        ts = int(dt_utc.timestamp())
        ts_ms = int(dt_utc.timestamp() * 1000)
        result = {
            "items": [
                {"title": f"{ts}", "subtitle": "时间戳（秒）｜按Cmd+C或回车将其复制到剪贴板", "arg": str(ts)},
                {"title": f"{ts_ms}", "subtitle": "时间戳（毫秒）｜按Cmd+C或回车将其复制到剪贴板", "arg": str(ts_ms)},
                {"title": f"{cn_str}", "subtitle": "中国本地时间（东八区）｜按Cmd+C或回车将其复制到剪贴板", "arg": cn_str},
                {"title": f"{utc_str}", "subtitle": "0时区时间（UTC）｜按Cmd+C或回车将其复制到剪贴板", "arg": utc_str}
            ]
        }
        print(json.dumps(result, ensure_ascii=False))
    except Exception as e:
        result = {
            "items": [
                {"title": "无法解析输入的时间", "subtitle": str(e), "arg": ""}
            ]
        }
        print(json.dumps(result, ensure_ascii=False))

def parse_time(input_str):
    input_str = input_str.strip()
    # 支持 now 关键字
    if input_str.lower() == 'now':
        return datetime.now(timezone.utc)
    # 支持时间戳（秒/毫秒）
    if re.fullmatch(r'-?\d{10,13}', input_str):
        ts = int(input_str)
        if len(input_str) >= 13:
            ts = ts / 1000
        return datetime.fromtimestamp(ts, tz=timezone.utc)
    # 支持常见时间字符串
    time_formats = [
        '%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M:%S', '%Y.%m.%d %H:%M:%S',
        '%Y-%m-%d %H:%M', '%Y/%m/%d %H:%M', '%Y.%m.%d %H:%M',
        '%Y-%m-%d', '%Y/%m/%d', '%Y.%m.%d',
        '%Y%m%d%H%M%S', '%Y%m%d',
        '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%dT%H:%M:%SZ',
    ]
    for fmt in time_formats:
        try:
            dt = datetime.strptime(input_str, fmt)
            return dt.replace(tzinfo=timezone(timedelta(hours=8))).astimezone(timezone.utc)
        except Exception:
            continue
    # 尝试用 dateutil 解析
    if dateutil:
        try:
            dt = dateutil.parser.parse(input_str)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone(timedelta(hours=8)))
            return dt.astimezone(timezone.utc)
        except Exception:
            pass
    raise ValueError('无法解析输入的时间')

if __name__ == "__main__":
    main()