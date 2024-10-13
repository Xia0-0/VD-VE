'''敏感信息泄露脚本，这里针对的是教育系统的敏感信息泄露。'''

# 导入模块
import requests                        # 用于发出HTTP请求，获取网页内容。
from bs4 import BeautifulSoup          # 用于解析网页内容，提取所需文本
from googlesearch import search        # 用于通过Google进行搜索，获取URL列表
import re                              # 导入正则表达式模块
import time                            # 提供与时间相关的功能
import random                          # 用于在请求之间引入随机延迟，模拟人类行为，避免被封
import os                              # 用于文件操作
from tqdm import tqdm                  # 用于显示进度条

# 关键词设置
query = "site:.cn (身份证 OR 身份编号 OR 姓名 OR 银行卡号 OR 手机号 OR 奖学金)"

# 身份证号和联系方式匹配正则表达式
sensitive_pattern = re.compile(
    r"\d{15}|\d{18}|\d{17}X|\d{16}|\d{3}-\d{8}|\d{4}-\d{7}", re.I
)

# 用于存储可疑网址
suspected_urls = []

# 定义屏蔽的网站
blocked_sites = [
    "baidu.com", 
    "gov.cn", 
    "google.com", 
    "facebook.com", 
    "twitter.com", 
    "zhihu.com",
    "tieba.baidu.com",
    "taobao.com"
]

# 设置搜索的数量和目标网址数
search_limit = 40  # 最大搜索结果数量
target_url_count = 10  # 找到多少个可疑网址后停止

# 执行搜索，直到找到目标数量的可疑网址
print("正在搜索中，请稍候...")
urls = list(search(query, num_results=search_limit))  # 注意使用 `num_results`
total_urls = len(urls)

# 遍历搜索结果，并检测敏感信息
for url in tqdm(urls, total=total_urls, desc="搜索进度"):
    
    # 检查网址是否在屏蔽列表中
    if any(blocked in url for blocked in blocked_sites):
        continue

    time.sleep(random.uniform(3, 5))  # 随机等待 2 到 5 秒，增加更长的间隔防止被封

    try:
        # 请求网页内容
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # 检查请求是否成功

        # 使用BeautifulSoup解析网页
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()

        # 检查网页内容是否包含敏感信息的关键字
        if sensitive_pattern.search(text) or any(
            keyword in text for keyword in ["身份证", "姓名", "身份编号"]
        ):
            suspected_urls.append(url)

        if len(suspected_urls) >= target_url_count:  # 如果已找到目标数量，结束循环
            break

    except requests.Timeout:
        print(f"请求超时: {url}")  # 处理超时错误
    except requests.RequestException as e:
        print(f"请求失败: {e}")  # 输出请求失败的信息
    except Exception as e:
        print(f"其他错误: {e}")  # 捕获所有其他可能的错误

# 检查文件是否存在
file_path = 'Suspected.txt'
if not os.path.exists(file_path):
    open(file_path, 'w').close()  # 如果不存在，先创建一个空文件

# 以追加模式打开文件
with open(file_path, 'a+') as f:
    f.seek(0)
    existing_urls = f.read().splitlines()
    new_urls = set(suspected_urls) - set(existing_urls)  # 找到新的可疑网址
    if new_urls:
        f.writelines(f"{url}\n" for url in new_urls)

print(f"已将 {len(new_urls)} 个可疑网址写入 Suspected.txt")
