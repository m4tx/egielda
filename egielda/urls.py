from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

js_info_dict = {
    'packages': ('egielda',),
}

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'egielda.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^manage/books/', include('books.urls')),
    url(r'^manage/categories/', include('categories.urls')),
    url(r'^sell/', include('sell.urls')),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
)
