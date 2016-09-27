from django_filters import FilterSet
from finder.models import Result, Query


class QueryFilter(FilterSet):

    class Meta:
        model = Query
        fields = ['query', 'status', ]


class ResultFilter(FilterSet):

    class Meta:
        model = Result
        fields = ['query__query', 'query__status', 'url', 'spider', 'rang', ]
