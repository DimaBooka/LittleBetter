from django.conf.urls import include
from appi import views
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    url(r'^query/$', views.query_list),
    url(r'^query/(?P<pk>[0-9]+)/$', views.query_detail),
    url(r'^result/$', views.result_list),
    url(r'^result/(?P<pk>[0-9]+)/$', views.result_detail),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns = format_suffix_patterns(urlpatterns)
