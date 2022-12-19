"""
2. Викорисовуючи Scrapy, написати скрипт, який буде приймати на вхід назву
   та ID категорії (у форматі назва/id/) із сайту https://rozetka.com.ua і
   буде збирати всі товари із цієї категорії, збирати по ним всі можливі дані
   (бренд, категорія, модель, ціна, рейтинг тощо) і зберігати їх у CSV файл
   (наприклад, якщо передана категорія mobile-phones/c80003/, то файл буде
   називатися c80003_products.csv)
"""
from RozetkaParser.spiders import rozetka
from scrapy.crawler import CrawlerProcess


if __name__ == '__main__':
    c = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0',
        'FEED_FORMAT': 'csv',
        'FEED_URI': rozetka.RozetkaScraper.category.replace('/', '_')+'.csv',
    })
    c.crawl(rozetka.RozetkaScraper)
    c.start()