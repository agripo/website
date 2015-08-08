from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render

import core.exceptions as core_exceptions


def index_view(request):
    print("User id : {}".format(request.session.get('_auth_user_id')))
    slideshow_images = [
        {'src': '/static/img/1.jpg', 'alt': 'One image', 'caption': 'Tayap est un petit village du Cameroun.'},
        {'src': '/static/img/2.jpg', 'alt': 'Another image', 'caption': 'Agripo est un groupement de Tayap.'},
    ]
    user = request.user
    return render(request, 'core/home_page.html',
                  {'display_slideshow': True, 'slideshow_images': slideshow_images, 'user': user})


def using_cookies_accepted(request):
    request.session['cookies_notification_shown'] = True
    return HttpResponse("OK")


def auto_connect(request, email):
    try:
        user = authenticate(email=email)
    except core_exceptions.NoAutoConnectionOnProductionServer:
        return HttpResponse("No autoconnection on production server")
    except core_exceptions.NoAutoConnectionWithExistingUser:
        return HttpResponse("No autoconnection with existing user")

    if user:
        # check if user is_active, and any other checks
        login(request, user)
        return HttpResponse("{} is connected".format(email))

    raise core_exceptions.AutoConnectionUnknownError("New user not found")

