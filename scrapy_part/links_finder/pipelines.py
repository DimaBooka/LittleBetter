# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import redis
import hashlib
import sqlalchemy
from sqlalchemy import select, update, func


class LinksFinderPipeline(object):

    def process_item(self, item, spider):
        """
        Provides an connection to sqlite DB and writing information-parse.

        :param:
            item: dicts of Item objects after parsing;
            spider: object of spider which is writing now;
        :return: an iterable of Item objects dicts.
        """
        try:
            con, meta = self.connect('postgres', 'tunnel', 'scraper')
            spider.log(u'Successfully connected sqlalchemy to postgres.')
        except:
            spider.log(u"Couldn't connect sqlalchemy to postgres.")
            return item

        queries = meta.tables['finder_query']
        query = queries.select().where(queries.c.query == item['query'][0])
        for q in con.execute(query):
            query = q

        try:
            item['urls'][0]
            spider.log(u'Links was found')
        except:
            query = hashlib.sha224(item['query'][0]).hexdigest()
            self.write_redis(query, item['spider'][0], spider)
            spider.log(u"Links didn't found.")
            return item

        i = 0
        for url in item.get('urls'):
            i += 1
            result = meta.tables['finder_result'].insert().values(query_id=query[0], url=url,
                                                                  spider=item['spider'][0],
                                                                  rang=i, date=func.now())
            con.execute(result)

        update_status = queries.update().where(meta.tables['finder_query'].c.id == query[0]).values(status='done')
        con.execute(update_status)

        query = hashlib.sha224(item['query'][0]).hexdigest()
        self.write_redis(query, item['spider'][0], spider)
        spider.log(u'Successfully closed %s spider.' % item['spider'][0])
        return item

    def connect(self, user, password, db, host='localhost', port=5432):
        '''
        Returns a connection and a metadata object
        '''
        url = 'postgresql://{}:{}@{}:{}/{}'
        url = url.format(user, password, host, port, db)
        con = sqlalchemy.create_engine(url, client_encoding='utf8')
        meta = sqlalchemy.MetaData(bind=con, reflect=True)

        return con, meta

    def write_redis(self, query, spidy, spider):
        """
        Connecting to redis-server and writes tuple - word-query:spider and status.

        :param:
            query: word-query from client;
            spidy: name of spiders which is writing now;
            spider: object-spider(just for logging);
        """
        try:
            red = redis.StrictRedis(host='localhost', port=6379, db=0)
            spider.log(u'Query: %s' % query)
            red.publish(query, "%s:%s" % (query, spidy))
            spider.log(u'Updated status for %s spider in Redis. %s' % (spidy, query))
        except:
            spider.log(u"Could'not connect to Redis.")
