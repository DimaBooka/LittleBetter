import scrapy
import json
from scrapy.loader import ItemLoader
from links_finder.items import LinksFinderItem


class GoogleSpider(scrapy.Spider):
    """
    Attributes:
         query: query-word from client;
         name: defines the name for this spider;
         allowed_domains: domains that this spider is allowed to crawl;
    """
    def __init__(self, query, **kwargs):
        super(GoogleSpider, self).__init__(**kwargs)
        self.query = query.replace('_', ' ')
    name = "google"
    allowed_domains = ["google.com.ua"]

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
        if not self.query:
            self.query = "mari"
        start_urls = ["https://www.google.com.ua/search?q=%s&tbm=isch&source=lnt&tbs=isz:l" % self.query.replace(' ', '+')]
        return start_urls

    def parse(self, response):
        """
        Method is in charge of processing the response and returning scraped data.

        :return: an iterable of Request and dicts of Item objects.
        """
        l = ItemLoader(item=LinksFinderItem(), response=response)
        links = list()
        urls = response.xpath('//*[@id="rg_s"]').xpath('.//*[@class="rg_meta"]/text()').extract()
        for image_url in urls:
            data = json.loads(image_url)
            links.append(data.get("ou"))
        l.add_value('query', self.query)
        l.add_value('spider', self.name)
        l.add_value('urls', links)
        return l.load_item()

