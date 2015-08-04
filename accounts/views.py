from django.contrib.auth import authenticate, login
from django.http import HttpResponse


def persona_login(request):
    user = authenticate(assertion=request.POST['assertion'])
    if user:
        login(request, user)
    return HttpResponse('OK')


def auto_connect(request, email):
    #    try:
    #        return self.get_user(email)
    #    except ListUser.DoesNotExist:
    #        return ListUser.objects.create(email=email)
    return HttpResponse("{} is connected".format(email))
