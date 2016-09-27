from django.conf.urls import url,include
from . import views


urlpatterns = [
    # url(r'^find/$', views.find, name='start'),
    url(r'^test/$', views.test, name='test'),
    # url(r'^(?P<query>\w+)', views.show, name='show'),
    # url(r'^', views.start, name='start'),
]
