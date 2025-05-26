from spiderv3 import get_response
import re

content = "杭州"
url = f"https://baike.baidu.com/item/{content}"
response = get_response(url)
print(response)

def extract_info(text):
    info = {
        "人口总量": None,
        "地区生产总值": None,
        "火车站": [],
        "著名景点": []
    }

    # 人口总量（支持匹配形如 "常住人口1262.4万人"）
    pop_match = re.search(r"(常住人口|人口数量)[：]?\s*([\d.]+)\s*万", text)
    if pop_match:
        info["人口总量"] = f"{pop_match.group(2)} 万"

    # 地区生产总值（如 21860亿元 或 21860 亿元）
    gdp_match = re.search(r"(地区生产总值)[：]?\s*([\d\s]+)\s*亿元", text)
    if gdp_match:
        info["地区生产总值"] = f"{gdp_match.group(2).strip()} 亿元"

    # 火车站（例如：杭州站、杭州东站、杭州南站、杭州西站）
    station_match = re.search(r"火车站[：]?\s*([^\n]+)", text)
    if station_match:
        station_str = station_match.group(1)
        stations = re.findall(r"[\u4e00-\u9fa5]+站", station_str)
        info["火车站"] = stations

    # 著名景点（例如：西湖、京杭大运河、西溪国家湿地公园、灵隐寺等）
    spot_match = re.search(r"(著名景点)[：]?\s*([^\n]+)", text)
    if spot_match:
        spot_str = spot_match.group(2)
        spots = re.findall(r"[\u4e00-\u9fa5·]+", spot_str)
        # 清理无效项和标点
        info["著名景点"] = [s for s in spots if len(s) >= 2]

    return info

info = extract_info(response)
print(info)
