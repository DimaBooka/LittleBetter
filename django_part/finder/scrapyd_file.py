from django.http import HttpResponseRedirect
from scrapyd_api import ScrapydAPI
# import redis
import logging
from.send_email import send_email as ALERT


logger = logging.getLogger(__name__)


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
            logger.info(u'Сonnected to Scrapyd.')
        except:
            ALERT()
            logger.error(u"Could'not connect to Scrapyd.")
            return HttpResponseRedirect('/')

        for spider in self.spiders:
            try:
                self.api.schedule('links_finder', spider, query=self.query)
                logger.info(u'Activated %s spider. ----- %s' % (spider, self.query))
            except:
                logger.warning(u"Could'not find %s spider." % spider)
                return HttpResponseRedirect('/')
