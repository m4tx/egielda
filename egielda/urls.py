# This file is part of e-Giełda.
# Copyright (C) 2014  Mateusz Maćkowski and Tomasz Zieliński
#
# e-Giełda is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# You should have received a copy of the GNU Affero General Public License
# along with e-Giełda.  If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

js_info_dict = {
    'packages': ('egielda',),
}

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'egielda.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^accounts/', include('authentication.urls')),

    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),

    url(r'^$', 'egielda.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^manage/', include('managemenu.urls')),
    url(r'^manage/books/', include('books.urls')),
    url(r'^manage/categories/', include('categories.urls')),
    url(r'^manage/sellers/', include('sellers.urls')),
    url(r'^manage/orders/', include('orders.urls')),
    url(r'^manage/stats/', include('stats.urls')),
    url(r'^manage/users/', include('users.urls')),
    url(r'^manage/settings/', include('settings.urls')),
    url(r'^sell/', include('sell.urls', namespace='sell')),
    url(r'^purchase/', include('purchase.urls', namespace='purchase')),
)
