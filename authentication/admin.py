# This file is part of e-Giełda.
# Copyright (C) 2014-2015  Mateusz Maćkowski and Tomasz Zieliński
#
# e-Giełda is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# You should have received a copy of the GNU Affero General Public License
# along with e-Giełda.  If not, see <http://www.gnu.org/licenses/>.

from django.contrib import admin
from django.contrib.auth.models import Permission

from authentication.models import AppUser, AppUserHasCorrectData


class AppUserAdmin(admin.ModelAdmin):
    exclude = ('is_superuser',)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'user_permissions':
            kwargs['queryset'] = Permission.objects.all().select_related('content_type')
        return super(AppUserAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

admin.site.register(AppUser, AppUserAdmin)
admin.site.register(AppUserHasCorrectData)
