from django.http import HttpResponse
from django.shortcuts import render


def index_view(request):
    slideshow_images = [
        {'src': '/static/img/1.jpg', 'alt': 'One image', 'caption': 'Tayap est un petit village du Cameroun.'},
        {'src': '/static/img/2.jpg', 'alt': 'Another image', 'caption': 'Agripo est un groupement de Tayap.'},
    ]
    return render(request, 'core/home_page.html', {'display_slideshow': True, 'slideshow_images':slideshow_images})


def using_cookies_accepted(request):
    request.session['cookies_notification_shown'] = True
    return HttpResponse("OK")
