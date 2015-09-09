from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.utils import timezone
from django.core.management import call_command

import core.exceptions as core_exceptions
from core.forms import CheckoutForm
from core.authentication import is_production_server
from core.models.news import News
from core.models.shop import Product, ProductCategory, Command
from core.models.general import SiteConfiguration, SITECONF_DEFAULT_NEWS_COUNT


def get_cart(request):
    """
    Sends a JSON object containing the products and quantities in current cart
    """
    cart_products = Product.static_get_cart_products()
    data = dict()
    data['products'] = []
    total = 0
    for cart_product in cart_products:
        product = Product.objects.get(id=cart_product['id'])
        product_total = cart_product['quantity'] * product.price
        data['products'].append(
            dict(id=cart_product['id'], name=product.name, quantity=cart_product['quantity'], price=product_total)
        )
        total += product_total

    data['total'] = total
    return JsonResponse(data)


def set_product_quantity(request, product=0, quantity=0):
    the_product = Product.objects.get(id=product)
    quantity = int(quantity)

    if not the_product.is_available():
        data = {'error': "NO_STOCK"}
    else:
        try:
            the_product.set_cart_quantity(quantity)
        except core_exceptions.AddedMoreToCartThanAvailable:
            data = {'error': "NOT_ENOUGH_STOCK", 'max': the_product.available_stock()}
        else:
            data = {"new_quantity": quantity}

    return JsonResponse(data)


class Checkout(CreateView):
    model = Command
    form_class = CheckoutForm
    template_name = "core/checkout.html"

    def get_success_url(self):
        return reverse("command_successfull")

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super().get_form_kwargs(**kwargs)
        form_kwargs["customer"] = self.request.user
        return form_kwargs

    def dispatch(self, request, *args, **kwargs):
        cart_products = Product.static_get_cart_products()
        if not cart_products:
            return redirect(reverse("shop_page"))

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart_products = Product.static_get_cart_products()
        context['products'] = []
        context['total'] = 0
        for product in cart_products:
            product_data = Product.objects.get(id=product['id'])
            product_total = product['quantity'] * product_data.price
            context['products'].append({
                'product': product_data,
                'quantity': product['quantity'],
                'total': product_total})
            context['total'] += product_total

        return context


class RequiresJs(TemplateView):
    template_name = "core/requires_js.html"

    def post(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back_link'] = self.request.GET['back']
        return context


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
            {'src': '/static/img/diapo_1.jpg', 'alt': 'One image',
             'caption': 'Tayap est un petit village du Cameroun.'},
            {'src': '/static/img/diapo_2.jpg', 'alt': 'Another image',
             'caption': 'Agripo est un groupement de Tayap.'},
            {'src': '/static/img/diapo_3.jpg', 'alt': 'A third image',
             'caption': 'Agripo est un groupement de Tayap.'},
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

        if request.GET and request.GET['as_farmer']:
            user.add_to_farmers()

        login(request, user)
        return HttpResponse("{} is connected as {}".format(email, connected_as))

    raise core_exceptions.AutoConnectionUnknownError("New user not found")
