from django.core.management import BaseCommand
import subprocess


class Command(BaseCommand):
    help = "Run autobahn"

    def handle(self, *args, **options):
        subprocess.check_output("python server.py", shell=True)
        self.stdout.write("DONE")
