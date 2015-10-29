from django.contrib.auth import authenticate, login
from django.contrib.flatpages.models import FlatPage
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.views.generic import ListView, DetailView, TemplateView, CreateView, FormView
from django.utils import timezone
from django.core.management import call_command
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

import core.exceptions as core_exceptions
from core.forms import CheckoutForm
from core.authentication import is_production_server
from core.models.news import News
from core.models.partners import Partner
from core.models.shop import Product, ProductCategory, Command, Delivery, Stock
from core.models.general import SiteConfiguration, SITECONF_DEFAULT_NEWS_COUNT
from core.models.users import AgripoUser


def get_cart(request):
    """
    Sends a JSON object containing the products and quantities in current cart
    """
    cart_products = Product.static_get_cart_products(request.user)
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
            the_product.set_cart_quantity(request.user, quantity)
        except core_exceptions.AddedMoreToCartThanAvailable:
            data = {'error': "NOT_ENOUGH_STOCK", 'max': the_product.available_stock()}
        else:
            data = {"new_quantity": quantity}

    return JsonResponse(data)


class UpdateStock(TemplateView):
    template_name = "core/update_stock.html"

    def post(self, request, *args, **kwargs):
        user = AgripoUser.objects.get(id=request.user.id)

        for key in request.POST:
            if "quantity." in key:
                product_id = int(key.replace("quantity.", ""))
                quantity = int(request.POST.get(key))
                Stock.objects.update_or_create(
                    farmer=user, product_id=product_id, defaults=dict(stock=quantity))

        message_text = "Stocks mis à jour avec succès"
        messages.add_message(request, messages.SUCCESS, message_text)
        return redirect(reverse("update_stock"))

    def products(self):
        user = self.request.user
        categories = ProductCategory.objects.all()
        products_list = []
        for category in categories:
            for product in category.product_set.all():
                farmers_stock = 0
                try:
                    stock = Stock.objects.get(farmer=user, product=product)
                    farmers_stock = stock.stock
                except Stock.DoesNotExist:
                    pass

                products_list.append(dict(product=product, stock=farmers_stock))

        return products_list


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
        cart_products = Product.static_get_cart_products(request.user)
        if not cart_products:
            return redirect(reverse("shop_page"))

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart_products = Product.static_get_cart_products(self.request.user)
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['intro'] = FlatPage.objects.get(url="/intro-liste-actualites/")
        return context

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
            {'src': '/static/img/slideshow/slideshow_1.jpg',
             'alt': 'Gestion durable des forêts.',
             'caption': 'Gestion durable des forêts.'},
            {'src': '/static/img/slideshow/slideshow_2.jpg',
             'alt': 'Cohésion sociale.',
             'caption': 'Cohésion sociale.'},
            {'src': '/static/img/slideshow/slideshow_3.jpg',
             'alt': "Diversification de l'économie locale.",
             'caption': "Diversification de l'économie locale."},
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


@staff_member_required
def delivery_details(request, id):
    template = 'admin/core/pastdelivery/details.html'
    delivery = Delivery.objects.get(pk=id)
    commands = Command.objects.filter(delivery=delivery)

    return render_to_response(template, {
        'title': 'Détails de la livraison "{}"'.format(delivery),
        'delivery': delivery,
        'commands': commands
    }, context_instance=RequestContext(request))
