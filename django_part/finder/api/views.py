from rest_framework import permissions, viewsets, status
from django.contrib.auth.models import User
from .serializers import QuerySerializer, ResultSerializer, UserSerializer
from finder.models import Query, Result
from rest_framework.filters import DjangoFilterBackend, OrderingFilter
from .filters import ResultFilter, QueryFilter
from rest_framework.response import Response


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class QueryViewSet(viewsets.ModelViewSet):
    queryset = Query.objects.all()
    serializer_class = QuerySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = QueryFilter
    ordering = 'query'

    def get_queryset(self):
        author = self.request.user.id
        return Query.objects.filter(author=author)


class ResultViewSet(viewsets.ModelViewSet):

    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_class = ResultFilter
    ordering = 'rang'
