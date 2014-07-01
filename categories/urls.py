from django.conf.urls import url

from categories import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^add$', views.add_category),
    url(r'^edit/([0-9]+)$', views.edit_category),
    url(r'^remove/([0-9,]+)$', views.remove_category),
]