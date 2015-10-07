from django.shortcuts import render_to_response


def get_focus(context, theme=None, focus=None):
    template_name = "webdoc/focus/theme{}_focus{}.html".format(theme, focus)
    return render_to_response(template_name=template_name)
