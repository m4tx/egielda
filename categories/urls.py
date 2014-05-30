from django.conf.urls import url

from categories import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
]