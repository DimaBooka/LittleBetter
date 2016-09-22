# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2
import redis
import hashlib


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
            con = psycopg2.connect("dbname='scraper' user='postgres' host='localhost' password='tunnel'")
            cur = con.cursor()
            spider.log(u'Successfully connected to postgres.')
        except:
            spider.log(u"Couldn't connect to postgres.")
            return item

        query = cur.execute("SELECT id FROM finder_query WHERE query='{0}'".format(item['query'][0]))
        query = cur.fetchone()

        try:
            item['urls'][0]
            spider.log(u'Links was found')
        except:
            query = hashlib.sha224(item['query'][0]).hexdigest()
            self.write_redis(query, item['spider'][0], spider)
            cur.close()
            con.close()
            spider.log(u"Links didn't found.")
            return item

        i = 0
        for url in item.get('urls'):
            i += 1
            sql = "INSERT INTO finder_result (query_id, url, spider, rang, date) " \
                  "VALUES ({0},'{1}','{2}',{3}, CURRENT_TIMESTAMP)".format(query[0], url, item['spider'][0], i)
            cur.execute(sql)
            con.commit()

        cur.execute("UPDATE finder_query SET status='{0}' WHERE id={1}".format('done', query[0]))
        con.commit()
        query = hashlib.sha224(item['query'][0]).hexdigest()
        self.write_redis(query, item['spider'][0], spider)
        cur.close()
        con.close()
        spider.log(u'Successfully closed %s spider.' % item['spider'][0])
        return item

    def write_redis(self, query, spidy, spider):
        """
        Connecting to redis-server and writes tuple - word-query:spider and status.

        :param:
            query: word-query from client;
            spidy: name of spiders which is writing now;
            spider: object-spider(just for logging);
        """
        # try:
        #     r = redis.Redis(host='localhost', port=6379, db=0)
        #     r.set("%s:%s" % (query, spidy), 'done')
        #     r.expire("%s:%s" % (query, spidy), 30)
        #     spider.log(u'Updated status for %s spider in Redis.' % spidy)
        # except:
        #     spider.log(u"Could'not connect to Redis.")

        try:
            red = redis.StrictRedis(host='localhost', port=6379, db=0)
            spider.log(u'Query: %s' % query)
            red.publish(query, "%s:%s" % (query, spidy))
            spider.log(u'Updated status for %s spider in Redis. %s' % (spidy, query))
        except:
            spider.log(u"Could'not connect to Redis.")
