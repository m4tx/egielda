from django.conf.urls import url

from dates import views


urlpatterns = [
    url(r'^$', views.index),
]