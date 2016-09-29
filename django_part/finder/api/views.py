from rest_framework import permissions, viewsets
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .serializers import QuerySerializer, ResultSerializer  # , UserSerializer
from finder.models import Query, Result
from rest_framework.filters import DjangoFilterBackend, OrderingFilter
from .filters import ResultFilter, QueryFilter

#
# class UserView(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = QuerySerializer
#

class QueryViewSet(viewsets.ModelViewSet):

    queryset = Query.objects.all()
    serializer_class = QuerySerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = QueryFilter
    ordering = 'query'


class ResultViewSet(viewsets.ModelViewSet):

    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = ResultFilter
    ordering = 'rang'
