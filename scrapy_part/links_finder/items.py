# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class LinksFinderItem(Item):
    query = Field()
    spider = Field()
    urls = Field()
    date = Field()
    status = Field()
    rang = Field()


