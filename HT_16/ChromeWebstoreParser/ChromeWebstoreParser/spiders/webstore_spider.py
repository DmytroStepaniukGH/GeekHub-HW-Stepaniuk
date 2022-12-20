from scrapy.spiders import SitemapSpider


class WebstoreSpider(SitemapSpider):
    name = 'webstore_spider'
    sitemap_urls = ["https://chrome.google.com/webstore/sitemap"]

    def parse(self, response):
        id = response.url.split('/')[-1]
        yield {
            'id': id if 'hl=' not in id else id.split('?')[0],
            'name': response.css("h1.e-f-w::text").get(),
            'description': response.css(".C-b-p-j-Pb::text").get()
        }
