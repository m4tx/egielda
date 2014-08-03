from django.conf.urls import url

from stats import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^sold/$', views.books_sold),
    url(r'^users/([0-9]+)/list/', views.list_books),
    url(r'^users/$', views.users),
    url(r'^books/$', views.books),
]