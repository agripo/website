from django.conf.urls import url

from admin_helper import views


urlpatterns = [
    url('^(?P<url>.*)/set_on_off/$', views.set_on_off, name='set_on_off'),
    url('^(?P<url>.*)/set_number/$', views.set_number, name='set_number'),
]
