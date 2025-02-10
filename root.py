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


class GetHotTitles:
    def __init__(self, url=None, headers=None):
        self.url = url
        self.headers = headers

    def fetch_titles(self, limit=None):
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            hot_titles = soup.find_all("div", class_="c-single-text-ellipsis", limit=limit)
            hot_titles_list = [item.get_text(strip=True) for item in hot_titles]
            return hot_titles_list
        except requests.exceptions.RequestException as e:
            print(f"爬取失败:{e}")
            return []


class MySqlHelper:
    def __init__(self, db_config=None):
        self.db_config = db_config

    def save_data(self, data_list, table="baidu_hot_search", column="title"):
        connection = None
        try:
            connection = connect(**self.db_config)
            if connection.is_connected():
                print("成功连接数据库")
            insert_query = f"INSERT INTO {table} ({column}) VALUES (%s)"
            with connection.cursor() as cursor:
                for data in data_list:
                    cursor.execute(insert_query, (data,))
                connection.commit()
                print("数据插入成功")
        except Error as e:
            print(f"数据库操作失败:{e}")
        finally:
            if connection and connection.is_connected():
                connection.close()
                print("数据库已关闭")


if __name__ == "__main__":
    spider = GetHotTitles(url, headers)
    hot_titles = spider.fetch_titles(limit=10)

    if hot_titles:
        print("爬取成功")
        db_saver = MySqlHelper(db_config)
        db_saver.save_data(hot_titles)
    else:
        print("未获取任何数据")
