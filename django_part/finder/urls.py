from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.views import login, logout
from . import views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm


urlpatterns = [
    url(r'^download/(?P<query>\w+)$', views.download),
    url(r'^login/$', login, {'template_name': 'index.html'}, name='login'),
    url(r'^logout/$', logout, {'template_name': 'index.html'}, name='logout'),
    url(r'^register/$', CreateView.as_view(template_name='user/registration.html',
                        form_class=UserCreationForm, success_url='/'), name='register'),
    url(r'^', TemplateView.as_view(template_name='index.html')),
]
