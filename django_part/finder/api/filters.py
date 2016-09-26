from django_filters import FilterSet
from finder.models import Result


class ResultFilter(FilterSet):

    class Meta:
        model = Result
        fields = ['query__query', 'query__status', 'url', 'spider', 'rang', ]
