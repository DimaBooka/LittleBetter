from finder.models import Query, Result
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('password', 'username',)
        read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined',)


class QuerySerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Query
        fields = '__all__'
        lookup_field = 'id'


class ResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Result
        fields = '__all__'
