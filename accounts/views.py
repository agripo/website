from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib.auth import get_user_model, SESSION_KEY

import accounts.exceptions as account_exceptions

User = get_user_model()


def persona_login(request):
    user = authenticate(assertion=request.POST['assertion'])
    if user:
        login(request, user)
    return HttpResponse('OK')


def auto_connect(request, email):
    try:
        user = authenticate(email=email)
    except account_exceptions.NoAutoConnectionOnProductionServer:
        return HttpResponse("No autoconnection on production server")
    except account_exceptions.NoAutoConnectionWithExistingUser:
        return HttpResponse("No autoconnection with existing user")

    if user:
        # check if user is_active, and any other checks
        login(request, user)
        return HttpResponse("{} is connected".format(email))

    raise account_exceptions.AutoConnectionUnknownError("New user not found")

