from django.conf.urls import url

from sell import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^personal/$', views.personal_data),
    url(r'^books/$', views.books),
    url(r'^summary/$', views.summary),
]