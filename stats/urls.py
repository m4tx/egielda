from django.conf.urls import url

from stats import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^sold/$', views.books_sold),
]