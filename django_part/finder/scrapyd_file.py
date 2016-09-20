from django.http import HttpResponseRedirect
from scrapyd_api import ScrapydAPI
# import redis
import logging
from.send_email import send_email as ALERT


logging.basicConfig(format=u'%(filename) 3s [LINE:%(lineno)d]# %(levelname)-3s [%(asctime)s] %(message)s',
                    level=logging.DEBUG, filename=u'all_logs.log')


class RunSpider:
    """
    Attributes:
        query: word-query from client;
        api: scrapyd api(you could check some information at this page);
        spiders: the list of spider which was defined at scrapyd-deploy;
    """
    def __init__(self, query):
        super(RunSpider, self).__init__()
        self.query = query
        self.api = None
        self.spiders = list()

    def run(self):
        """
        If connection to scrapyd is OK, runs spiders, and write in Redis tuple - word-query:spider and status.

        :return: in case disconnection with scrapyd or redis redirect to main page;
        """
        try:
            self.api = ScrapydAPI('http://0.0.0.0:6800')
            self.spiders = self.api.list_spiders('links_finder')
            logging.info(u'Сonnected to Scrapyd.')
        except:
            ALERT()
            logging.error(u"Could'not connect to Scrapyd.")
            return HttpResponseRedirect('/')

        for spider in self.spiders:
            try:
                self.api.schedule('links_finder', spider, query=self.query)
                logging.info(u'Activated %s spider. ----- %s' % (spider, self.query))
            except:
                logging.warning(u"Could'not find %s spider." % spider)
                return HttpResponseRedirect('/')
            # try:
            #     r = redis.Redis(host='localhost', port=6379, db=0)
            #     r.set("%s:%s" % (self.query, spider), 'create')
            #     r.expire("%s:%s" % (self.query, spider), 60)
            #     logging.info(u'Wrote to Redis.')
            # except:
            #     ALERT()
            #     logging.error(u"Could'not connect to Redis.")
            #     return HttpResponseRedirect('/')
