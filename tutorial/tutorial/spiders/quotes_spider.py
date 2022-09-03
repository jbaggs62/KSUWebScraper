# import scrapy
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor
# import re
# from tld import get_tld
# from bs4 import BeautifulSoup as BS
# import hashlib
# from tutorial.items import WebsiteItem

# class EmailSpider(CrawlSpider):
#     name = "kennesaw"
#     emailRegex = re.compile(r"[-.a-z]+@[^@\s\.]+\.[.a-z]{2,3}")
#     allowed_domains = ['kennesaw.edu']
#     start_urls = [
#         'https://www.kennesaw.edu',
#         'https://ccse.kennesaw.edu',
#         'https://research.kennesaw.edu'
#         ]
#     rules = (
#         Rule(LinkExtractor(allow=()), callback='parse', follow=True, unqiue),
#     )
#     def parse(self, response):
#         self.logger.info('Hi, this is an item page! %s', response.url)
#         entry = WebsiteItem()
#         entry[pageID]=hashlib.md5(response.url.encode()).hexdigest()
#         entry[url]=response.url
#         entry[title]=response.xpath('//title/text()').getall()[0],
#         entry[body]=' '.join(BS(response.text).get_text(separator=' ').split())
#         # entry = {
#         #     'pageid': hashlib.md5(response.url.encode()).hexdigest(),
#         #     'url': response.url,
#         #     'title': response.xpath('//title/text()').getall()[0],
#         #     'body': ' '.join(BS(response.text).get_text(separator=' ').split())
#         # }
#         entry['emails'] = re.findall(self.emailRegex, entry['body'])
#         yield entry


# class GatherEmails(scrapy.Spider):
#     name = 'ksu_email_gather'
#     allowed_domains = ['kennesaw.edu']
#     start_urls = ['https://kennesaw.edu']
#     greedy = True
#     email_regex = re.compile(r"[-.a-z]+@[^@\s\.]+\.[.a-z]{2,3}")
#     forbidden_keys = ['tel:', 'mailto:', '.jpg', '.pdf', '.png']
#     CLOSESPIDER_PAGE_COUNT: 1000


#     def parse(self, response):
#         try:
#             html = response.body.decode('utf-8')
#         except UnicodeDecodeError:
#             return
#         body_emails = self.email_regex.findall(html)
#         emails = [email for email in body_emails if \
#                 get_tld('https://' + email.split('@')[-1], fail_silently=True)]
#         yield {
#             'emails': list(set(emails)),
#             'page': response.request.url
#         }
#         if self.greedy:
#             links = response.xpath("//a/@href").getall()
#             # If there are external links, scrapy will block them
#             # because of the allowed_domains setting
#             for link in links:
#                 skip = False
#                 for key in self.forbidden_keys: 
#                     if key in link:
#                         skip = True
#                         break
#                 if skip:
#                     continue
#                 try:
#                     yield scrapy.Request(link, callback=self.parse)
#                 except ValueError:
#                     try:
#                         yield response.follow(link, callback=self.parse)
#                     except:
#                         pass
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
