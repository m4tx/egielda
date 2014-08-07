from django.conf.urls import url

from sellers import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^([0-9]+)/accept/([0-9]+)/edit/', views.accept_edit_book),
    url(r'^([0-9]+)/accept/', views.accept_books),
    url(r'^([0-9,]+)/remove/', views.remove_seller),
    url(r'^bulk/(\w+)/$', views.bulk_actions),
]