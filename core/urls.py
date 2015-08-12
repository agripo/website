from core.authentication import is_staging_server, is_development_server
from django.conf.urls import url, patterns
from django.contrib.auth.views import logout
from django.views.generic import RedirectView

from core import views


urlpatterns = [
    url(r'^$', views.index_view, name="home_page"),
    url(r'^logout$', logout, {'next_page': '/'}, name='logout'),
    url(r'using_cookies_accepted', views.using_cookies_accepted, name="using_cookies_accepted"),
    url(r'news$', views.NewsListPage.as_view(), name="news_page"),
    url(r'news/(?P<pk>[0-9]+)$', views.NewsPage.as_view(), name="one_news_page"),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
]

if is_staging_server() or is_development_server():
    urlpatterns += patterns(
        '',
        url(r'^core/auto_login/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]+)$',
            views.auto_connect, {'manager': False}, name='auto_connect'),
        url(r'^core/auto_manager_login/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]+)$',
            views.auto_connect, {'manager': True}, name='auto_manager_connect'),
    )
