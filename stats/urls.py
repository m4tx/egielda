from django.conf.urls import url

from stats import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^sold/$', views.books_sold),
    url(r'^users/$', views.users),
    url(r'^users/list/([0-9]+)/', views.list_books),
    url(r'^books/$', views.books),
]