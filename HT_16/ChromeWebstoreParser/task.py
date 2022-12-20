"""
1. Використовуючи Scrapy, заходите на
   "https://chrome.google.com/webstore/sitemap", переходите на кожен лінк з
   тегів <loc>, з кожного лінка берете посилання на сторінки екстеншинів,
   парсите їх і зберігаєте в CSV файл ID, назву та короткий опис кожного
   екстеншена (пошукайте уважно де його можна взяти). Наприклад:
   “aapbdbdomjkkjkaonfhkkikfgjllcleb”, “Google Translate”,
   “View translations easily as you browse the web. By the Google
   Translate team.”
"""
from ChromeWebstoreParser.spiders import webstore_spider
from scrapy.crawler import CrawlerProcess


if __name__ == '__main__':
    c = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0',
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'ChromeWebstoreFixId.csv',
    })
    c.crawl(webstore_spider.WebstoreSpider)
    c.start()