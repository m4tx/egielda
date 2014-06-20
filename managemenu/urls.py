from django.conf.urls import url

from managemenu import views


urlpatterns = [
    url(r'^$', views.index),
]