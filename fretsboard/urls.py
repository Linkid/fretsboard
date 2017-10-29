"""fretsboard URL Configuration."""

from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^', include('scoreboard.urls')),
]
