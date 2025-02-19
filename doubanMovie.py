import re
import time
import random
import requests
from bs4 import BeautifulSoup
from tools.crawlerTool import CrawlerTool as BaseCrawlerTool
from tools.mySqlHelper import MySqlHelper as BaseMySqlHelper
from mysql.connector import connect, Error

def extract_text(item, selector, attr=None):
    element = item.select_one(selector)
    if not element:
        return None
    return element.get(attr) if attr else element.get_text(strip=True)

class DoubanMovieCrawler(BaseCrawlerTool):
    """重写的Douban爬虫类，继承自CrawlerTool"""
    def fetch_data(self, limit=None):
        """重写fetch_data，使用优化后的Cookie和动态User-Agent"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Cookie": 'dbcl2="287095374:/c4tU3fh3x4"; ck=nRWr'
        }
        try:
            session = requests.Session()
            session.headers.update(headers)
            response = session.get(self.url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            print(f"Request successful with User-Agent: {headers['User-Agent']}")
            return self.parse_data(soup, limit)
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return []


    def parse_data(self, soup, limit=None):
        movies = []
        items = soup.select('div.item')
        for item in items[:limit] if limit else items:
            title = extract_text(item, 'span.title')
            rating = float(extract_text(item, 'span.rating_num'))
            num_raters = int(extract_text(item, 'div.star span:last-child').replace('人评价', ''))
            quote = extract_text(item, 'span.inq')
            info = item.select_one('div.bd p').get_text(strip=True)
            year = re.search(r'\d{4}', info)
            year = int(year.group(0)) if year else None  # 确保符合YEAR类型
            director = info.split('/')[0].strip()
            actors = info.split('/')[-1].strip() if '/' in info else None
            genres = extract_text(item, 'span.genre')
            link = extract_text(item, 'a', 'href')

            movies.append((title, rating, num_raters, quote, director, actors, year, genres, link))

        return movies

class MySqlHelper(BaseMySqlHelper):
    """重写的MySqlHelper类，动态生成SQL插入语句"""
    def save_data(self, data_list, table):
        connection = None
        if not data_list:
            print("No data to save.")
            return
        columns = ['title', 'rating', 'num_raters', 'quote', 'director', 'actors', 'release_date', 'genres', 'link']
        placeholders = ', '.join(['%s'] * len(columns))
        column_names = ', '.join(columns)
        insert_query = f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})"

        try:
            connection = connect(**self.db_config)
            with connection.cursor() as cursor:
                cursor.executemany(insert_query, data_list)
                connection.commit()
                print("Data inserted successfully into movies table")
        except Error as e:
            print(f"Database operation failed: {e}")
        finally:
            if connection and connection.is_connected():
                connection.close()

def fetch_all_pages(base_url, pages=None):
    """分页爬取所有页面数据"""
    all_movies = []
    for i in range(pages):
        url = f"{base_url}&start={i*25}"
        crawler = DoubanMovieCrawler(url, None)
        all_movies.extend(crawler.fetch_data())
    return all_movies

if __name__ == "__main__":
    base_url = "https://movie.douban.com/top250?filter="
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '321227',
        'database': 'spider_data'
    }

    movie_data = fetch_all_pages(base_url, pages=8)
    db_helper = MySqlHelper(db_config)
    db_helper.save_data(movie_data, 'movies')
