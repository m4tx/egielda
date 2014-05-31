from django.conf.urls import url

from books import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^add/$', views.add_book),
    url(r'^edit/([0-9]+)/$', views.edit_book),
    url(r'^remove/([0-9,]+)/$', views.remove_book),
    url(r'^bulk/(\w+)/$', views.bulk_actions),
]