import scrapy
from scrapy.loader import ItemLoader
from links_finder.items import LinksFinderItem
import json
import re


class InstagramSpider(scrapy.Spider):
    """
    Attributes:
         query: query-word from client;
         name: defines the name for this spider;
         allowed_domains: domains that this spider is allowed to crawl;
    """
    def __init__(self, query, **kwargs):
        super(InstagramSpider, self).__init__(**kwargs)
        self.query = query.replace('_', ' ')
    name = "instagram"
    allowed_domains = ["instagram.com"]

    def start_requests(self):
        """
        Called by Scrapy when the spider is opened for scraping.

        :return: an iterable with the first Requests to crawl for this spider;
        """
        links = self.get_links()
        for link in links:
            yield self.make_requests_from_url(link)

    def get_links(self):
        """
        Forming a URLs for parsing.

        :return: a list of URLs where the spider will begin to crawl from;
        """
        start_urls = ["https://www.instagram.com/explore/tags/" + self.query.replace(' ', '_') + "/"]
        return start_urls

    def parse(self, response):
        """
        Method is in charge of processing the response and returning scraped data.

        :return: an iterable of Request and dicts of Item objects.
        """
        l = ItemLoader(item=LinksFinderItem(), response=response)
        like_json = "".join(response.xpath('//script[contains(text(), "sharedData")]/text()').extract())
        all_data = json.loads("".join(re.findall(r'window._sharedData = (.*);', like_json)))

        first = all_data['entry_data']['TagPage'][0]['tag']['media']['nodes']
        second = all_data['entry_data']['TagPage'][0]['tag']['top_posts']['nodes']
        all_links = first + second

        final_links = []
        for link in all_links:
            final_links.append(link['display_src'][:link['display_src'].find('?ig_')])

        links = list()
        for link in final_links:
            links.append(link)

        l.add_value('query', self.query)
        l.add_value('spider', self.name)
        l.add_value('urls', links)
        return l.load_item()