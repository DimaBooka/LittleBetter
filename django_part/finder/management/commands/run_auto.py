from django.core.management import BaseCommand
from server import *


class Command(BaseCommand):
    help = "Run autobahn"

    def handle(self, *args, **options):
        run()
