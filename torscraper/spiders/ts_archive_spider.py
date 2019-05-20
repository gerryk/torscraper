import scrapy


class TorScraperSpider(scrapy.Spider):
    name = "torarchiver"

    def __init__(self):
        self.url_file = "urls"
        self.urls = []
        try:
            with open(self.url_file) as fh:
                for line in fh:
                    self.urls.append(line.strip())
        except:
            print "URLs file not available"
            exit


    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = "torscraper-%s.html" % page
        with open(filename, 'wb') as f:
            f.write(response.body)
            print filename
        self.log('Saved file %s' % filename)
        next_page = response.css('a::attr(href)').get()
        if next_page is not None and "mailto" not in next_page:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
