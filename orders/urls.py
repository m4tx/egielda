from django.conf.urls import url

from orders import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^notexecuted/$', views.not_executed),
    url(r'^outdated/$', views.outdated),
    url(r'^executed/$', views.executed),
    url(r'^([0-9]+)/execute/$', views.execute),
    url(r'^([0-9]+)/execute/accept/$', views.execute_accept),
    url(r'^([0-9]+)/$', views.order_details),
]