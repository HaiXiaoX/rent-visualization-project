import unittest
from crawler import Crawler

class TestCrawler(unittest.TestCase):
    def setUp(self):
        # 用 config 文件初始化
        self.crawler = Crawler(config_file='config.json')

    def test_get_random_proxy(self):
        proxy = self.crawler.get_random_proxy()
        self.assertIsInstance(proxy, dict)

    def test_parse_page_empty(self):
        listings = self.crawler.parse_page("")
        self.assertIsInstance(listings, list)
        self.assertEqual(len(listings), 0)

    def test_parse_page_fake_html(self):
        fake_html = """
        <div class="content__list--item">
            <p class="content__list--item--title">测试房源</p>
            <span class="content__list--item-price">5000元/月</span>
            <span class="content__list--item--area">80㎡</span>
            <div class="content__list--item--des">天河-员村</div>
        </div>
        """
        listings = self.crawler.parse_page(fake_html)
        self.assertGreaterEqual(len(listings), 1)
        self.assertIn('测试房源', listings[0][0])

if __name__ == '__main__':
    unittest.main()
