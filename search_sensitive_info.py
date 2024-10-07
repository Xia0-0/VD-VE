import requests
from bs4 import BeautifulSoup
from googlesearch import search
import time
import random

# 关键词设置
query = "身份证 edu"

# 用于存储可疑网址
suspected_urls = []

# 定义屏蔽的网站
blocked_sites = ["baidu.com", "gov.cn"]

# 执行搜索
for url in search(query, num_results=20):
    # 检查网址是否在屏蔽列表中
    if any(blocked in url for blocked in blocked_sites):
        continue

    time.sleep(random.uniform(1, 3))  # 随机等待 1 到 3 秒

    if len(suspected_urls) >= 10:
        break
    try:
        # 请求网页内容
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # 抛出HTTP错误

        # 使用BeautifulSoup解析网页
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()

        # 检查网页内容是否包含敏感信息的关键字
        if any(keyword in text for keyword in ["身份证", "姓名", "edu"]):
            suspected_urls.append(url)

    except requests.RequestException as e:
        print(f"请求失败: {e}")
        continue

# 将可疑网址写入文件
with open('Suspected.txt', 'w') as f:
    f.write('\n'.join(suspected_urls))

print("已将可疑网址写入 Suspected.txt")
