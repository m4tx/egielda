from django.conf.urls import url

from students import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^unaccepted/$', views.unaccepted),
    url(r'^list/([0-9]+)/', views.list_books),
    url(r'^accept/([0-9]+)/', views.accept_books),
]