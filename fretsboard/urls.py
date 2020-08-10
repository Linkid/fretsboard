"""fretsboard URL Configuration."""

from django.conf.urls import include
from django.conf.urls import re_path
from django.contrib import admin

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
    re_path(r'^', include('scoreboard.urls')),
]
