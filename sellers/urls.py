from django.conf.urls import url

from sellers import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^([0-9]+)/accept/', views.accept_books),
    url(r'^([0-9]+)/accept/edit/([0-9]+)/', views.accept_edit_book),
]