from django.conf.urls import url
from django.views.generic import RedirectView

from core import views


urlpatterns = [
    url(r'^$', views.index_view, name="home_page"),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
]
