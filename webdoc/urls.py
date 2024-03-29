from django.conf.urls import url
from webdoc.views import get_focus
from django.views.generic.base import TemplateView


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="webdoc/index.html"), name="home_page"),
    url(r'^webdoc$', TemplateView.as_view(template_name="webdoc/webdoc.html"), name='webdoc'),
    url(r'^project$', TemplateView.as_view(template_name="webdoc/project.html"), name='project'),
    url(r'^support$', TemplateView.as_view(template_name="webdoc/support.html"), name='support'),
    url(r'^partners$', TemplateView.as_view(template_name="webdoc/partners.html"), name='partners'),
    url(r'^credits$', TemplateView.as_view(template_name="webdoc/credits.html"), name='credits'),
    url(r'^focus/theme(?P<theme>[0-9])_focus(?P<focus>[0-9])/$', get_focus, name='focus'),
]
