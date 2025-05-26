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
    random_sleep_time = random.randint(100, 2000) / 1000.0  # 将毫秒转换为秒
    # 随机睡眠
    time.sleep(random_sleep_time)
    print(url)
    # 发送HTTP请求并获取响应
    response = requests.get(url)

    contents = []
    # 检查响应状态码，确保请求成功
    if response.status_code == 200:
        # 解析HTML内容
        soup = BeautifulSoup(response.text, "html.parser")

        # 找到class属性为"lemmaSummary_M04mg", "J-summary"的div元素
        div_with_class_summary = soup.find_all("div", class_=re.compile(r"\bJ-summary\b"))

        # 找到class属性为"J-lemma-content"的div元素
        div_with_class = soup.find("div", class_="J-lemma-content")

        # 使用find_all查找所有class属性中包含"J-summary"的div
        j_summary_divs = soup.find_all("div", class_=re.compile(r"\bJ-summary\b"))
        # print(j_summary_divs)
        # 打印结果
        for div in j_summary_divs:
            # 找到所有在div_container中的span元素
            span_elements = div.find_all("span")
            tmp = ""

            # 遍历所有span元素并输出内容
            for span in span_elements:

                if span.get("class") and has_text(span.get("class")):
                    tmp += span.text
            contents.append(tmp)
            contents.append("\n")

        if div_with_class:

            # 遍历div中的所有子元素
            for child in div_with_class.descendants:
                tmp_1 = ""
                # 检查子元素是否是span标签且class属性为"text_wRvkv"
                if child.name == "div" and child.get("class") and has_para_content_mark(child.get("class")):
                    # 打印span元素的文本内容
                    for new_child in child.descendants:
                        if new_child.name == "span" and new_child.get("class") and has_text(new_child.get("class")):
                            tmp_1 += new_child.text
                    contents.append(tmp_1)
                    contents.append("\n")

                    #  检查子元素是否是h2标签
                elif child.name == "h2":
                    # 打印h2标签的内容
                    contents.append("####\n" + child.text + "\n")
                elif child.name == "h3":
                    # 打印h2标签的内容
                    contents.append("##" + child.text + "\n")
        return "".join(contents)

    else:
        return "Failed to retrieve the{}.".format(url)

# 发送HTTP请求并获取响应
if __name__ == '__main__':
    content = "杭州"
    url=f"https://baike.baidu.com/item/{content}"
    response = get_response(url)
    print(response)
