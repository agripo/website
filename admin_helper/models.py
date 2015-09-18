from django.db.models import IntegerField, BooleanField


def admin_helper_on_off(field):

    def setter(self):
        if not isinstance(field, BooleanField):
            raise Exception("This field should be an Integer or one of its descendants")

        value = getattr(self, field.name)
        url = '{}/{}/set_on_off/'.format(self._get_pk_val(), field.name)
        gif = '<img class="admin_helper_on_off" src="/static/admin/img/icon-{}.gif" alt="{}" />'.format(('no', 'yes')[value], value)
        return '<a href ="{}">{}</a>'.format(url, gif)

    setter.short_description = field.verbose_name
    setter.allow_tags = True
    return setter


def admin_helper_number(field, step=1):

    def setter(self):
        if not isinstance(field, IntegerField):
            raise Exception("This field should be an Integer or one of its descendants")

        value = getattr(self, field.name)

        def get_link(num, side):
            num = value + num if side == "+" else value - num
            url = '{}/{}/set_number/?number={}'.format(self._get_pk_val(), field.name, num)
            return '&nbsp;<a href="{}">{}</a>&nbsp;'.format(url, num)

        ret = ""
        for i in [3 * step, 2 * step, step]:
            ret = ret + get_link(i, '-')

        ret += "<strong>{}</strong>".format(value)
        for i in [step, 2 * step, 3 * step]:
            ret = ret + get_link(i + 1, '+')

        return '<span class="admin_helper_number">{}</span>'.format(ret)

    setter.short_description = field.verbose_name
    setter.allow_tags = True
    return setter
