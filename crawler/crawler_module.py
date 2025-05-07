import requests
from bs4 import BeautifulSoup
import csv
import os
import random
import time
import json
import re
import logging

class Crawler:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.url = ''
        self.site = ''
        self.output_file = ''
        self.max_retries = 3
        self.proxies_pool = []
        self.selectors = {
            'lianjia': {
                'item': 'div.content__list--item',
                'title': 'p.content__list--item--title a',
                'price': 'span.content__list--item-price em',
                'area': 'p.content__list--item--des',
                'location': 'p.content__list--item--des a'
            }
        }
        self.load_config()
        self.setup_logger()

    def setup_logger(self):
        if not os.path.exists('log'):
            os.makedirs('log')
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s [%(levelname)s] %(message)s',
                            handlers=[
                                logging.FileHandler("log/crawler.log", encoding='utf-8'),
                                logging.StreamHandler()
                            ])

    def load_config(self):
        if not os.path.exists(self.config_file):
            logging.error(f"❌ 配置文件未找到: {self.config_file}")
            return
        with open(self.config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            crawler_cfg = config.get('crawler', {})
            self.url = crawler_cfg.get('url', '')
            self.site = crawler_cfg.get('site', '')
            self.output_file = crawler_cfg.get('output_file', 'data/rent_data.csv')
            self.max_retries = crawler_cfg.get('max_retries', 3)
            self.proxies_pool = crawler_cfg.get('proxies_pool', [])

    def fetch_page(self, url):
        headers = {'User-Agent': 'Mozilla/5.0'}
        for attempt in range(self.max_retries):
            try:
                proxies = random.choice(self.proxies_pool) if self.proxies_pool else None
                response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
                if response.status_code == 200:
                    logging.info(f"✅ 成功获取页面: {url}")
                    return response.text
                else:
                    logging.warning(f"⚠️ 状态码异常: {response.status_code}")
            except Exception as e:
                logging.warning(f"⚠️ 请求失败: {e}, 重试 {attempt + 1}/{self.max_retries}")
                time.sleep(random.uniform(1, 3))
        logging.error("❌ 超过最大重试次数，获取页面失败")
        return None

    def parse_page(self, html):
        if not html:
            logging.error("❌ HTML 为空，跳过解析")
            return []
        if self.site not in self.selectors:
            logging.error(f"❌ 未知 site 配置: {self.site}")
            return []

        soup = BeautifulSoup(html, 'html.parser')
        listings = []
        s = self.selectors[self.site]

        try:
            for listing in soup.select(s['item']):
                title = listing.select_one(s['title']).get_text(strip=True) if listing.select_one(s['title']) else 'N/A'
                price = listing.select_one(s['price']).get_text(strip=True) + '元/月' if listing.select_one(s['price']) else 'N/A'

                des_block = listing.select_one(s['area']).get_text(strip=True) if listing.select_one(s['area']) else ''
                area_match = re.search(r'(\d+\.?\d*)㎡', des_block)
                area = area_match.group(0) if area_match else 'N/A'

                location_tags = listing.select(s['location'])
                location = ' - '.join([tag.get_text(strip=True) for tag in location_tags]) if location_tags else 'N/A'

                listings.append([title, price, area, location])
            logging.info(f"✅ 解析出 {len(listings)} 条房源")
        except Exception as e:
            logging.error(f"❌ HTML 解析出错: {e}")
        return listings

    def save_to_csv(self, data):
        if not data:
            logging.error("❌ 无数据保存")
            return
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        try:
            with open(self.output_file, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(['Title', 'Price', 'Area', 'Location'])
                writer.writerows(data)
            logging.info(f"✅ 数据已保存到 {self.output_file}")
        except Exception as e:
            logging.error(f"❌ 保存数据失败: {e}")

    def run(self):
        html = self.fetch_page(self.url)
        if html:
            data = self.parse_page(html)
            if data:
                self.save_to_csv(data)
            else:
                logging.error("❌ 页面解析失败，无数据可保存")
        else:
            logging.error("❌ 页面获取失败，终止爬虫任务")
