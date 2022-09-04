import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import hashlib
from bs4 import BeautifulSoup as BS
import re


class emailCrawler(CrawlSpider):
    name = 'ksu'
    allowed_domains = ['kennesaw.edu']
    start_urls = [
        'https://www.kennesaw.edu',
        'https://ccse.kennesaw.edu',
        'https://research.kennesaw.edu'
        ]
    emailRegex = re.compile(r"[-.a-z]+@[^@\s\.]+\.[.a-z]{2,3}")
    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=()), callback='parse_item'),

    )
    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        # item = scrapy.Item()
        # item['id'] = id + 1
        # item['url'] = response.url
        # item['title'] = response.xpath('//title/text()').getall()[0],
        # item['body'] = ' '.join(BS(response.text).get_text(separator=' ').split())
        entry = {
            'pageid': hashlib.md5(response.url.encode()).hexdigest(),
            'url': response.url,
            'title': response.xpath('//title/text()').getall()[0],
            'body': ' '.join(BS(response.text).get_text(separator=' ').split())
        }
        entry['emails'] = re.findall(self.emailRegex, entry['body'])
        yield entry
        if url is not None:
            return response.follow(url, self.parse_additional_page, cb_kwargs=dict(entry=entry))

    def parse_additional_page(self, response, entry):
        entry['additional_data'] = response.xpath('//p[@id="additional_data"]/text()').get()
        return entry
