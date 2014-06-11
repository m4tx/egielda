from django.conf.urls import url

from students import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^unaccepted/$', views.unaccepted),
    url(r'^unaccepted/list/([0-9]+)/$', views.unaccepted_list_books),
    url(r'^unaccepted/accept/([0-9]+)/edit/([0-9]+)/', views.accept_edit_book),
    url(r'^unaccepted/accept/([0-9]+)/', views.accept_books),
    url(r'^list/([0-9]+)/', views.list_books),
]