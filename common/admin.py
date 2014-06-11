from django.contrib import admin
from common.models import AppUser, BookType, Book, Purchase

admin.site.register(AppUser)
admin.site.register(BookType)
admin.site.register(Book)
admin.site.register(Purchase)
