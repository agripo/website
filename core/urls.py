from core.authentication import is_staging_server, is_development_server
from django.conf.urls import url, patterns
from django.contrib.auth.views import logout
from django.views.generic import RedirectView

from core import views


urlpatterns = [
    url(r'^$', views.index_view, name="home_page"),
    url(r'^logout$', logout, {'next_page': '/'}, name='logout'),
    url(r'using_cookies_accepted/$', views.using_cookies_accepted, name="using_cookies_accepted"),
    url(r'news/$', views.NewsListPage.as_view(), name="news_page"),
    url(r'shop/$', views.ShopPage.as_view(), name="shop_page"),
    url(r'shop/checkout$', views.checkout, name="checkout"),
    url(r'shop/get_cart$', views.get_cart, name="get_cart"),
    url(r'^shop/set_product_quantity/(?P<product>[0-9]+)/(?P<quantity>[0-9]+)/', views.set_product_quantity,
        name="set_product_quantity"),
    url(r'^requires_js$', views.RequiresJs.as_view(), name="requires_js"),
    url(r'menu_(?P<page>[a-z_]+)/$', views.SubMenusPage.as_view(), name="menu_page"),
    url(r'news/(?P<pk>[0-9]+)/$', views.NewsPage.as_view(), name="one_news_page"),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/shared/favicon.ico', permanent=True)),
]

if is_staging_server() or is_development_server():
    urlpatterns += patterns(
        '',
        url(r'^core/auto_login/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]+)$',
            views.auto_connect, {'manager': False}, name='auto_connect'),
        url(r'^core/auto_manager_login/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]+)$',
            views.auto_connect, {'manager': True}, name='auto_manager_connect'),
        url(r'^core/populatedb/(?P<news_count>[0-9]+)/(?P<products_count>[0-9]+)/(?P<categories_count>[0-9]+)/$',
            views.populate_db, name='populate_db'),
    )
