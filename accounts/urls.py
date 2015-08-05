from agripo_website.settings import SERVER_TYPE
from django.conf.urls import url, patterns
from django.contrib.auth.views import logout

from accounts import views


urlpatterns = [
    url(r'^login$', views.persona_login, name='persona_login'),
    url(r'^logout$', logout, {'next_page': '/'}, name='logout'),
]


if SERVER_TYPE == "STAGING" or SERVER_TYPE == "DEVELOPMENT":
    urlpatterns += patterns(
        '',
        url(r'^auto_login/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]+)$', views.auto_connect, name='auto_connect'),
    )
