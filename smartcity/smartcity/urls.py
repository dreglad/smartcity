"""smartcity URL Configuration"""
from django.conf.urls import url
from django.contrib import admin

admin.site.site_header = 'City Towers Grand'

urlpatterns = [
    url(r'^', admin.site.urls),
]
