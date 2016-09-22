from rest_framework import permissions
from rest_framework import viewsets
from .serializers import QuerySerializer, ResultSerializer
from finder.models import Query, Result


class QueryViewSet(viewsets.ModelViewSet):

    queryset = Query.objects.all()
    serializer_class = QuerySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ResultViewSet(viewsets.ModelViewSet):

    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
