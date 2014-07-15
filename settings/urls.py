from django.conf.urls import url

from settings import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^dates/$', views.dates),
]