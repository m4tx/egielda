from django.conf.urls import url

from books import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^add/$', views.add_book),
    url(r'^([0-9,]+)/$', views.book_details),
    url(r'^([0-9]+)/edit/$', views.edit_book),
    url(r'^([0-9,]+)/remove/$', views.remove_book),
    url(r'^bulk/(\w+)/$', views.bulk_actions),
]