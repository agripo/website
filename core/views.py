from core.models import News
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.utils import timezone

import core.exceptions as core_exceptions


NUMBER_OF_NEWS_BY_PAGE = 10


class ShopPage(TemplateView):
    template_name = "core/shop_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = [
            {'name': 'Fruits', 'products': [
                {'name': 'Bananes', 'stock': 10, 'bought': 1, 'img': 'bananes.jpg'},
                {'name': 'Mandarines', 'stock': 10, 'bought': 1, 'img': 'mandarines.jpg'},
                {'name': 'Citron', 'stock': 5, 'bought': 2, 'img': 'citrons.jpg'}, ]},
            {'name': 'Noix et produits du cacao', 'products': [
                {'name': 'Fèves de cacao', 'stock': 1, 'bought': 0, 'img': 'cacao.jpg'},
                {'name': 'Jus de cacao', 'stock': 0, 'bought': 0, 'img': 'cacao.jpg'},
                {'name': 'Bitter-cola', 'stock': 5, 'bought': 2, 'img': 'bitter.jpg'},
                {'name': 'Noix de Cola', 'stock': 12, 'bought': 1, 'img': 'cola.jpg'}, ]},
            {'name': 'Légumes', 'products': [
                {'name': 'Avocats', 'stock': 3, 'bought': 3, 'img': 'avocats.jpg'},
                {'name': 'Manioc', 'stock': 15, 'bought': 2, 'img': 'manioc.jpg'},
                {'name': 'Arbres à ail', 'stock': 15, 'bought': 1, 'img': 'ail.jpg'}, ]},
        ]
        return context


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
    paginate_by = NUMBER_OF_NEWS_BY_PAGE

    def get_queryset(self):
        return News.objects.filter(
            publication_date__lte=timezone.now(), is_active=True).order_by('-publication_date')

def index_view(request):
    slideshow_images = [
        {'src': '/static/img/diapo_1.jpg', 'alt': 'One image', 'caption': 'Tayap est un petit village du Cameroun.'},
        {'src': '/static/img/diapo_2.jpg', 'alt': 'Another image', 'caption': 'Agripo est un groupement de Tayap.'},
        {'src': '/static/img/diapo_3.jpg', 'alt': 'A third image', 'caption': 'Agripo est un groupement de Tayap.'},
    ]
    user = request.user
    return render(request, 'core/home_page.html',
                  {'display_slideshow': True, 'slideshow_images': slideshow_images, 'user': user})


def using_cookies_accepted(request):
    request.session['cookies_notification_shown'] = True
    return HttpResponse("OK")


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
