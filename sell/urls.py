from django.conf.urls import url

from sell import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
]