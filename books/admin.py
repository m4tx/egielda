from django.contrib import admin

from books.models import BookType, Book


admin.site.register(BookType)
admin.site.register(Book)