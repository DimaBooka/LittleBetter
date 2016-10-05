from django.apps import AppConfig


class FinderConfig(AppConfig):
    name = 'finder'
    verbose_name = 'Finder Application'

    def ready(self):
        import finder.signals
