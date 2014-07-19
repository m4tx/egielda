from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from orders import views


urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy(views.not_executed)), name='orders.views.index'),
    url(r'^notexecuted/$', views.not_executed),
    url(r'^outdated/$', views.outdated),
    url(r'^executed/$', views.executed),
]