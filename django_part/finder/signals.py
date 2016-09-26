from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Query
from .scrapyd_file import run
import logging


logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Query)
def run_spider(sender, instance, raw=True, **kwargs):
    run(instance.query)
