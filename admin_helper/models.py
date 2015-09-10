from django.db.models import IntegerField, BooleanField


def on_off_setter(field):

    def setter(self):
        if not isinstance(field, BooleanField):
            raise Exception("This field should be an Integer or one of its descendants")

        value = getattr(self, field.name)
        url = '{}/{}/set_on_off/'.format(self._get_pk_val(), field.name)
        gif = '<img src="/static/admin/img/icon-{}.gif" alt="{}" />'.format(('no', 'yes')[value], value)
        return '<a href ="{}">{}</a>'.format(url, gif)

    setter.short_description = field.verbose_name
    setter.allow_tags = True
    return setter


def number_setter(field, width=30):

    def setter(self):
        if not isinstance(field, IntegerField):
            raise Exception("This field should be an Integer or one of its descendants")

        value = getattr(self, field.name)
        url = '{}/{}/set_number/'.format(self._get_pk_val(), field.name)
        input = '<input name="number" type="number" value="{}" style="width:{}px"/>'.format(value, width)
        submit = '<input type="image" src="/static/admin/img/icon_changelink.gif"/>'
        form = '<form action="{}" method="GET">{}{}</form>'.format(url, input, submit)
        return form

    setter.short_description = field.verbose_name
    setter.allow_tags = True
    return setter
