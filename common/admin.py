from django.contrib import admin

from common.models import AppUser, Book, Purchase, Setting


admin.site.register(AppUser)
admin.site.register(Book)
admin.site.register(Purchase)
admin.site.register(Setting)
