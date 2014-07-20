from django.conf.urls import url

from sellers import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^accept/([0-9]+)/edit/([0-9]+)/', views.accept_edit_book),
    url(r'^accept/([0-9]+)/', views.accept_books),
]