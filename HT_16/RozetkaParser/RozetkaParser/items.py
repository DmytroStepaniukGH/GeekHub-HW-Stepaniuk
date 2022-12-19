import scrapy


class ProductItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    category = scrapy.Field()
    price = scrapy.Field()


