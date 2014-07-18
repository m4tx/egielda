from django.contrib import admin

from common.models import AppUser, Book, Purchase


admin.site.register(AppUser)
admin.site.register(Book)
admin.site.register(Purchase)
