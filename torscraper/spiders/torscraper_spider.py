import scrapy


class TorScraperSpider(scrapy.Spider):
    name = "torscraper"

    def start_requests(self):
        urls = [
            '',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        yield {
            'title': response.css('title').get(),
            'heading': response.css('h1').get(),
            'links': response.css('a').getall()
        }
