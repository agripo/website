from django.conf.urls import url

from admin_helper import views


urlpatterns = [
    url('^(?P<url>.*)/admin_helper_model_structure/$', views.model_structure, name='set_on_off'),
    url('^(?P<url>.*)/set_on_off/$', views.set_on_off, name='set_on_off'),
    url('^(?P<url>.*)/set_number/$', views.set_number, name='set_number'),
    url('^(?P<url>.*)/set_text/$', views.set_text, name='set_text'),
]
