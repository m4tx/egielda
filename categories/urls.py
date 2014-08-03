from django.conf.urls import url

from categories import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^add/$', views.add_category),
    url(r'^([0-9]+)/list/$', views.list_books),
    url(r'^([0-9]+)/edit/$', views.edit_category),
    url(r'^([0-9]+)/remove/$', views.remove_category),
]