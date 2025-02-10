import re

import requests
from bs4 import BeautifulSoup
from mysql.connector import connect, Error

url = "https://top.baidu.com/board?tab=realtime"
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
}

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "321227",
    "database": "spider_data"
}


class GetHotSearch:
    """操作MySQL数据库的类"""

    def __init__(self, url=None, headers=None):
        """
         初始化爬虫类
         :param url: 目标网页的URL
         :param headers: 请求头，防止被反爬
        """
        self.url = url
        self.headers = headers

    def fetch_searchs(self, limit=None):
        """
       获取百度热搜榜的标题
       :param limit: 限制获取的热搜数量
       :return: 返回一个包含热搜标题的列表
       """
        try:
            # 发送get请求获取网页内容
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()

            # 用BeatifulSoup 解析网页内容
            soup = BeautifulSoup(response.text, "html.parser")

            # 找到所有符合热搜标题的html元素并提取返回列表
            hot_items = soup.find_all("div", class_="category-wrap_iQLoo", limit=limit)
            hot_data = []
            for item in hot_items:
                # 获取标题
                title_tag = item.find("div", class_="c-single-text-ellipsis")
                title = title_tag.get_text(strip=True) if title_tag else "未知标题"
                # 获取内容

                content_tag = item.find("div", class_=re.compile(r"hot-desc_.*"))
                content = content_tag.get_text(strip=True) if content_tag else "暂无内容"

                hot_data.append((title, content))

            return hot_data

        except requests.exceptions.RequestException as e:
            print(f"爬取失败:{e}")
            return []


class MySqlHelper:
    """操作MySQL数据库的类"""

    def __init__(self, db_config=None):
        """
         初始化数据库连接
         :param db_config: 包含数据库配置信息的字典
        """
        self.db_config = db_config

    def save_data(self, data_list, table="baidu_hot_search"):
        """
        将爬取的数据保存到MySQL数据库
        :param data_list: 需要存储的热搜标题列表
        :param table: 目标数据库表名
        :param column: 目标数据表的列名
        """
        connection = None
        try:
            # 连接数据库
            connection = connect(**self.db_config)
            if connection.is_connected():
                print("成功连接数据库")

            # 插入数据的SQL语句
            insert_query = f"INSERT INTO {table} (title,content) VALUES (%s, %s)"

            # 使用游标执行sql
            with connection.cursor() as cursor:
                # 批量插入数据 (title, content)
                cursor.executemany(insert_query, data_list)
                connection.commit()
                print("数据插入成功")

        except Error as e:
            print(f"数据库操作失败:{e}")
        finally:
            if connection and connection.is_connected():
                connection.close()
                print("数据库已关闭")


if __name__ == "__main__":
    # 创建爬虫对象并获取热搜标题
    spider = GetHotSearch(url, headers)
    hot_items = spider.fetch_searchs(limit=10)

    if hot_items:
        print("爬取成功")
        # 创建数据库助手对象，并将数据存入数据库
        db_saver = MySqlHelper(db_config)
        db_saver.save_data(hot_items)
    else:
        print("未获取任何数据")
