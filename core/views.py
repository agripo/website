from django.http import HttpResponse
from django.shortcuts import render


def index_view(request):
    return render(request, 'core/home_page.html', {})


def using_cookies_accepted(request):
    request.session['cookies_notification_shown'] = True
    return HttpResponse("OK")
