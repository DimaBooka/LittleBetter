from finder.models import Query, Result
from rest_framework import serializers
# from django.contrib.auth.models import User
#
#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('password', 'first_name', 'last_name', 'email',)
#         write_only_fields = ('password',)
#         read_only_fields = ('is_staff', 'is_superuser', 'is_active', 'date_joined',)
#
#     def restore_object(self, attrs, instance=None):
#         user = super(UserSerializer, self).restore_object(attrs, instance)
#         user.set_password(attrs['password'])
#         return user
#

class QuerySerializer(serializers.ModelSerializer):

    class Meta:
        model = Query
        fields = '__all__'
        lookup_field = 'id'


class ResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Result
        fields = '__all__'
