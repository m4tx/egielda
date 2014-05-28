from django.conf.urls import url

from books import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add/$', 'books.views.add_book'),
    url(r'^edit/([0-9]+)/$', 'books.views.edit_book'),
    url(r'^remove/([0-9,]+)/$', 'books.views.remove_book'),
]