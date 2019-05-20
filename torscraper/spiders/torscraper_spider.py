import scrapy
import re
import os


class TorScraperSpider(scrapy.Spider):
    name = "torscraper"
    def __init__(self):
        self.url_file = "urls"
        self.search_file = "searchkeys"
        self.urls = []
        self.search = {}
        if os.path.isfile(self.search_file):
            with open(self.search_file) as fh:
                for line in fh:
                    k, v = line.strip().split(' ', 1)
                    self.search[k] = v.strip()
        try:
            with open(self.url_file) as fh:
                for line in fh:
                    self.urls.append(line.strip())
        except:
            print "URLs file not available"
            exit


        print self.search

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.logger.info("starting parsing engine...")
        btc = re.compile('[13][a-km-zA-HJ-NP-Z1-9]{25,34}')
        page = response.url.split("/")[-2]
        search_results = []
        self.logger.info(self.search)
        for k in self.search:
            search_results.append(response.xpath("//*[contains(text(), '{}')]".format(self.search[k])).extract())
        links = response.css('a').getall()
        mail_links = [ l for l in links if 'mail' in l]
        usernames = [ l for l in links if 'user' in l]
        btc_addrs = []
        for l in links:
            m = re.search('[13][a-km-zA-HJ-NP-Z1-9]{24,33}', l)
            if m is not None:
                btc_addrs.append(m.group(0))
        yield {
            'title': response.css('title').get(),
            'heading': response.css('h1').get(),
            'email': mail_links,
            'BTC address': btc_addrs,
            'links': links,
            'usernames': usernames,
            'search_results': search_results,
        }
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

