from finder.models import Query, Result
from rest_framework import serializers


class QuerySerializer(serializers.ModelSerializer):
    query = serializers.CharField(read_only=True)

    class Meta:
        model = Query
        fields = '__all__'
        lookup_field = 'id'


class ResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Result
        fields = '__all__'
