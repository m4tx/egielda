from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.views.generic import TemplateView

admin.autodiscover()

js_info_dict = {
    'packages': ('egielda',),
}

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'egielda.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^accounts/login/', login, name='login'),
    url(r'^accounts/logout/', logout, name='logout'),

    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),

    url(r'^$', TemplateView.as_view(template_name='egielda/home.html'), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^manage/', include('managemenu.urls')),
    url(r'^manage/books/', include('books.urls')),
    url(r'^manage/categories/', include('categories.urls')),
    url(r'^manage/users/', include('users.urls')),
    url(r'^sell/', include('sell.urls')),
    url(r'^purchase/', include('purchase.urls')),
)
