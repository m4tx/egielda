from django.contrib import admin

from common.models import AppUser, Book


admin.site.register(AppUser)
admin.site.register(Book)
