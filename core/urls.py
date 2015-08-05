from django.conf.urls import url
from django.views.generic import RedirectView


urlpatterns = [
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico', permanent=True))
]
