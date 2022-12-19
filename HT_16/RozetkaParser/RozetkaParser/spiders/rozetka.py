import re
import scrapy


class RozetkaScraper(scrapy.Spider):
    name = 'rozetka_parser'
    category = 'jacks/c329355'
    start_urls = ["https://rozetka.com.ua/"+category]

    def parse(self, response):
        for link in response.css('a.goods-tile__picture.'
                                 'ng-star-inserted::attr(href)'):
            yield response.follow(link.get(), callback=self.parse_item)

        pagination_link = response.css('a.button.button--gray.button--medium.'
                                       'pagination__direction.pagination__'
                                       'direction--forward.'
                                       'ng-star-inserted').attrib['href']
        yield response.follow(pagination_link, self.parse)

    def parse_item(self, response):
        yield{
            'id': re.sub(r'[^0-9]', '',
                         response.css("p.product__code."
                                      "detail-code::text").get().strip()),
            'name': response.css("h1.product__title::text").get().strip(),
            'category': response.css("li.breadcrumbs__item.breadcrumbs__"
                                     "item--last."
                                     "ng-star-inserted span::text").get(),
            'price': re.sub(r'[^0-9]', '',
                            response.css('.product-prices__'
                                         'big::text').get().strip())
        }
