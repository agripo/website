from django.contrib.auth import authenticate, login
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.utils import timezone
from django.core.management import call_command

import core.exceptions as core_exceptions
from core.authentication import is_production_server
from core.models import SiteConfiguration, ProductCategory, News, SITECONF_DEFAULT_NEWS_COUNT


class SubMenusPage(TemplateView):

    def get_template_names(self):
        return 'core/submenus/{}.html'.format(self.kwargs['page'])


class ShopPage(ListView):
    template_name = "core/shop_page.html"
    model = ProductCategory
    context_object_name = "categories"


class NewsPage(DetailView):
    model = News

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav_previous'] = context['object'].get_previous()
        context['nav_next'] = context['object'].get_next()
        return context


class NewsListPage(ListView):
    template = "core/news_list.html"
    context_object_name = "news_list"

    def get_queryset(self):
        return News.objects.filter(
            publication_date__lte=timezone.now(), is_active=True).order_by('-publication_date')

    def get_paginate_by(self, queryset):
        try:
            config = SiteConfiguration.objects.get()
            count = config.news_count
        except SiteConfiguration.DoesNotExist:
            count = SITECONF_DEFAULT_NEWS_COUNT
        return count


def index_view(request):
    slideshow_images = {
        'carousel_id': 'home_main_carousel',
        'images': [
            {'src': '/static/img/diapo_1.jpg', 'alt': 'One image', 'caption': 'Tayap est un petit village du Cameroun.'},
            {'src': '/static/img/diapo_2.jpg', 'alt': 'Another image', 'caption': 'Agripo est un groupement de Tayap.'},
            {'src': '/static/img/diapo_3.jpg', 'alt': 'A third image', 'caption': 'Agripo est un groupement de Tayap.'},
        ]
    }
    user = request.user
    return render(request, 'core/home_page.html',
                  {'display_slideshow': True, 'slideshow_images': slideshow_images, 'user': user})


def using_cookies_accepted(request):
    request.session['cookies_notification_shown'] = True
    return HttpResponse("OK")


def populate_db(request, news_count, products_count, categories_count):
    if is_production_server():
        return Http404()

    call_command('populatedb',
                 news_count=news_count, products_count=products_count, categories_count=categories_count)
    return HttpResponse('<div id="ok">Successfully created {} news</div>'.format(news_count))


def auto_connect(request, email, manager=False):
    try:
        user = authenticate(email=email)
    except core_exceptions.NoAutoConnectionOnProductionServer:
        return HttpResponse("No autoconnection on production server")
    except core_exceptions.NoAutoConnectionWithExistingUser:
        return HttpResponse("No autoconnection with existing user")

    if user:
        # check if user is_active, and any other checks
        if manager:
            user.add_to_managers()
            connected_as = "manager"
        else:
            connected_as = "user"

        login(request, user)
        return HttpResponse("{} is connected as {}".format(email, connected_as))

    raise core_exceptions.AutoConnectionUnknownError("New user not found")
