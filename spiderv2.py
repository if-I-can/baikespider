import requests
from bs4 import BeautifulSoup
import time
import re
import random


# 百度百科会增加一些字段，例如para_df21d,para_fr44h,需要识别
def has_para_content_mark(child_class):
    i = 0
    for t in child_class:
        if t[0:5] == "para_":
            i += 1
        if t[0:5] == "MARK_":
            i += 1
        if t[0:8] == "content_":
            i += 1
    return i == 3


# 百度百科会增加一些字段，例如text_sd55g4,text_fw92g,需要识别
def has_text(child_class):
    i = 0
    for t in child_class:
        if t[0:5] == "text_":
            i += 1
    return i == 1


# 爬取内容，并解析出开头的简介和正文内容
def get_response(url):
    random_sleep_time = random.randint(100, 2000) / 1000.0
    time.sleep(random_sleep_time)
    print("Requesting:", url)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    contents = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # 找到主要内容容器
        main_wrapper = soup.find("div", id="J-lemma-main-wrapper")
        if not main_wrapper:
            return "无法找到词条主体内容。"

        # 找到真正的内容容器
        content_wrapper = main_wrapper.find("div", class_=lambda x: x and "contentWrapper" in x)
        if not content_wrapper:
            return "未找到正文内容区域。"

        # 提取所有段落和标题
        for tag in content_wrapper.find_all(["div", "h2", "h3"]):
            cls = tag.get("class", [])
            text = tag.get_text(strip=True)
            if not text:
                continue
            # 判断是否是标题
            if any("title" in c.lower() for c in cls):
                contents.append("####\n" + text + "\n")
            elif any("para" in c.lower() or "paragraph" in c.lower() for c in cls):
                contents.append(text + "\n")
            else:
                # 有时正文段落直接是无 class 的 <div>
                if tag.name == "div" and not cls and len(text) > 30:
                    contents.append(text + "\n")

        return "".join(contents)

    else:
        return f"请求失败，状态码: {response.status_code}"


# 发送HTTP请求并获取响应
if __name__ == '__main__':
    content = "杭州"
    url = f"https://baike.baidu.com/item/{content}"
    response = get_response(url)
    print(response)
