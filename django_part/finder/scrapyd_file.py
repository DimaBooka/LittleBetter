from requests.packages.urllib3.exceptions import ConnectionError
from scrapyd_api import ScrapydAPI, exceptions
from django.conf import settings
from .errors import RunSpiderError
import logging
from.send_email import send_email as ALERT


logger = logging.getLogger(__name__)


def run(query):
    """
    If connection to scrapyd is OK, runs spiders, and write in Redis tuple - word-query:spider and status.
    query: word-query from client;
        api: scrapyd api(you could check some information at this page);
        spiders: the list of spider which was defined at scrapyd-deploy;
    :return: in case disconnection with scrapyd or redis redirect to main page;
    """
    try:
        api = ScrapydAPI(settings.SCRAPYD_API)
        spiders = api.list_spiders(settings.SCRAPY_APP)
        logger.info(u'Сonnected to Scrapyd.')
    except:
        ALERT()
        logger.error(u"Could'not connect to Scrapyd.")
        raise RunSpiderError(u"Could'not connect to Scrapyd.")

    for spider in spiders:
        try:
            api.schedule('links_finder', spider, query=query)
            logger.info(u'Activated %s spider. %s' % (spider, query))
        except exceptions.ScrapydResponseError:
            logger.warning(u"Could'not find %s spider." % spider)
            raise RunSpiderError(u"Could'not find %s spider." % spider)
