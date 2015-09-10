from django.contrib import messages
from django.apps import apps
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied


def _prepare(request, url):
    app_label, model_name, object_id, field = url.split('/')
    model = apps.get_model(app_label=app_label, model_name=model_name)

    object = get_object_or_404(model, pk=object_id)
    user = request.user
    if not user.has_perm("{}.{}".format(app_label, model_name), object):
        raise PermissionDenied

    return object, field


def set_number(request, url):
    object, field = _prepare(request, url)
    if request.method != 'GET':
        raise Exception("Wrong protocol : Only GET is valid")

    value = request.GET["number"]
    setattr(object, field, int(value))
    object.save()

    msg = 'Value changed to successfully'.format(value)
    messages.add_message(request, messages.SUCCESS, msg)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def set_on_off(request, url):
    object, field = _prepare(request, url)
    setattr(object, field, getattr(object, field) == 0)
    object.save()

    msg = '"%s" flag changed for %s' % (field, object)
    messages.add_message(request, messages.SUCCESS, msg)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
