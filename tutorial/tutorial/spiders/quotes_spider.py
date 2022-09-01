import scrapy
from scrapy.spiders import CrawlSpider
import re
from tld import get_tld
from bs4 import BeautifulSoup as BS
import hashlib

class EmailSpider(CrawlSpider):
    name = "kennesaw"
    emailRegex = re.compile(r"[-.a-z]+@[^@\s\.]+\.[.a-z]{2,3}")
    start_urls = [
        'https://www.kennesaw.edu',
        # 'https://csse.kennesaw.edu',
        # 'https://research.kennesaw.edu'
        ]
    def parse(self, response):
        entry = {
            'pageid': hashlib.md5(response.url.encode()).hexdigest(),
            'url': response.url,
            'title': response.xpath('//title/text()').getall()[0],
            'body': ' '.join(BS(response.text).get_text(separator=' ').split())
        }
        entry['emails'] = re.findall(self.emailRegex, entry['body'])

        yield entry 
