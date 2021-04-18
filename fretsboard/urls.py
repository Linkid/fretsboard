"""fretsboard URL Configuration."""

from django.contrib import admin
from django.urls import include
from django.urls import re_path

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^i18n/', include('django.conf.urls.i18n')),
    re_path(r'^', include('scoreboard.urls')),
]
