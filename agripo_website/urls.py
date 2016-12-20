"""agripo_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.contrib import auth

from core import urls as core_urls
from django.conf import settings
from django.contrib.auth.views import logout
from django.contrib.flatpages import views as flatpages_views
from registration.backends.hmac.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail


urlpatterns = [
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url(r'^accounts/register/$', RegistrationView.as_view(form_class=RegistrationFormUniqueEmail),
        name='registration_register'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^accounts/login/$', auth.views.login, name='account_login'),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^admin/', include('admin_helper.urls')),
    url(r'^webdoc/', include('webdoc.urls', namespace="webdoc")),
    url(r'', include(core_urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<url>.*/)$', flatpages_views.flatpage),
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT}))
