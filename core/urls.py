from core.authentication import is_staging_server, is_development_server
from django.conf.urls import url, patterns
from django.contrib.auth.views import logout
from django.views.generic import RedirectView, TemplateView, ListView
from django.views.decorators.cache import never_cache

from core import views
from core.models.partners import Partner


urlpatterns = [
    url(r'^$', views.index_view, name="home_page"),
    url(r'^logout$', logout, {'next_page': '/'}, name='logout'),
    url(r'^using_cookies_accepted/$', views.using_cookies_accepted, name="using_cookies_accepted"),
    url(r'^news/$', views.NewsListPage.as_view(), name="news_page"),
    url(r'^care/$', views.CareListPage.as_view(), name="care_page"),
    url(r'^partners/$', ListView.as_view(
        model=Partner, template_name='core/partners_page.html', context_object_name="partners"), name="partners_page"),
    url(r'^shop/(?P<pk>[0-9]+)/$', views.ShopPage.as_view(), name="shop_page"),
    url(r'^shop/checkout$', never_cache(views.Checkout.as_view()), name="checkout"),
    url(r'^shop/get_cart$', never_cache(views.get_cart), name="get_cart"),
    url(r'^shop/update_stock$', never_cache(views.UpdateStock.as_view()), name="update_stock"),
    url(r'^admin/core/delivery/(?P<id>[0-9]+)/details/$', views.delivery_details, name="delivery_details"),
    url(r'^shop/command_successfull', TemplateView.as_view(
        template_name="core/command_successfull.html"), name="command_successfull"),
    url(r'^shop/set_product_quantity/(?P<product>[0-9]+)/(?P<quantity>[0-9]+)/',
        never_cache(views.set_product_quantity), name="set_product_quantity"),
    url(r'^requires_js$', views.RequiresJs.as_view(), name="requires_js"),
    url(r'^menu_(?P<page>[a-z_]+)/$', views.SubMenusPage.as_view(), name="menu_page"),
    url(r'^news/(?P<pk>[0-9]+)/$', views.NewsPage.as_view(), name="one_news_page"),
    url(r'^care/(?P<pk>[0-9]+)/$', views.CarePage.as_view(), name="one_care_page"),
    url(r'^reservation/$', views.ReservationView.as_view(), name="reservation_page"),
    url(r'^reservation_ok/$', TemplateView.as_view(
        template_name="core/reservation_ok.html"), name="reservation_ok_page"),
    url(r'^backup/$', views.get_backup, name="backup"),
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
