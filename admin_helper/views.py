from django.contrib import messages
from django.apps import apps
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied


from django.db.models.fields import AutoField

def _prepare(request, url):
    app_label, model_name, object_id, field = url.split('/')
    model = apps.get_model(app_label=app_label, model_name=model_name)

    object = get_object_or_404(model, pk=object_id)
    user = request.user
    if not user.has_perm("{}.change_{}".format(app_label, model_name)):
        raise PermissionDenied

    return object, field


def model_structure(request, url):
    app_label, model_name = url.split('/')
    model = apps.get_model(app_label=app_label, model_name=model_name)

    fields = []
    integers = ["PositiveIntegerField", "IntegerField", "PositiveSmallIntegerField", "SmallIntegerField",
                "BigIntegerField"]
    for field in model._meta.fields:
        type = field.get_internal_type()
        if type in integers:
            data = {'name': field.name, 'type': "IntegerField", 'django_type': type}
            if type == "BigIntegerField":
                data['min'] = -9223372036854775808
                data['max'] = 9223372036854775807

            else:
                if "Small" in type:
                    data['min'] = -32768
                    data['max'] = 32767
                else:
                    data['min'] = -2147483648
                    data['max'] = 2147483647

                if "Positive" in type:
                    data['min'] = 0

            fields.append(data)

        elif type in ["BooleanField", "CharField"]:
            fields.append(
                {'name': field.name, 'type': type}
            )

    return JsonResponse({'fields': fields})


def _set_data(request, url, value):
    object, field = _prepare(request, url)
    if request.method != 'GET':
        raise Exception("Wrong protocol : Only GET is valid")

    setattr(object, field, value)
    object.save()

    msg = '{} of item #{} changed successfully'.format(field, object.pk)
    messages.add_message(request, messages.SUCCESS, msg)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def set_number(request, url):
    return _set_data(request, url, int(request.GET["value"]))


def set_text(request, url):
    return _set_data(request, url, request.GET["value"])


def set_on_off(request, url):
    object, field = _prepare(request, url)
    value = getattr(object, field) == 0
    setattr(object, field, value)
    object.save()

    msg = 'The state of {} on item #{} changed successfully to {}'.format(field, object.pk, value)
    messages.add_message(request, messages.SUCCESS, msg)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
