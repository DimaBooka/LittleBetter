import scrapy
import json
from scrapy.loader import ItemLoader
from links_finder.items import LinksFinderItem


class YandexSpider(scrapy.Spider):
    """
    Attributes:
         query: query-word from client;
         name: defines the name for this spider;
         allowed_domains: domains that this spider is allowed to crawl;
    """
    def __init__(self, query, **kwargs):
        super(YandexSpider, self).__init__(**kwargs)
        self.query = query.replace('_', ' ')
    name = "yandex"
    allowed_domains = ["yandex.ua"]

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
        start_urls = ["https://yandex.ua/images/search?text=" + self.query.replace(' ', '+') + "&rdpass=1"]
        return start_urls

    def parse(self, response):
        """
        Method is in charge of processing the response and returning scraped data.

        :return: an iterable of Request and dicts of Item objects.
        """
        l = ItemLoader(item=LinksFinderItem(), response=response)
        like_json = response.xpath('//*[contains(@class, "serp-item_group_search")]').xpath('./@data-bem').extract()
        final_links = [json.loads(arr)['serp-item']['img_href'] for arr in like_json]

        links = list()
        for link in final_links:
            if not link.endswith('.html'):
                links.append(link)

        l.add_value('query', self.query)
        l.add_value('spider', self.name)
        l.add_value('urls', links)
        return l.load_item()
