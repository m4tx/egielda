# This file is part of e-Giełda.
# Copyright (C) 2014  Mateusz Maćkowski and Tomasz Zieliński
#
# e-Giełda is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404

from books.forms import BookForm
from books.models import BookType
from utils.alerts import set_success_msg


@permission_required('common.view_books_index', raise_exception=True)
def index(request):
    book_list = BookType.objects.all().order_by('title')
    return render(request, 'books/index.html', {'book_list': book_list})


@permission_required('common.view_books_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.visible = True
            book.save()
            form.save_m2m()
            set_success_msg(request, 'book_added')
            return HttpResponseRedirect(reverse(index))
    else:
        form = BookForm()
    return render(request, 'books/add.html', {'form': form})


@permission_required('common.view_books_edit_book', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(BookType, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            book.visible = True
            book.save()
            form.save_m2m()
            set_success_msg(request, 'book_edited')
            return HttpResponseRedirect(reverse(index))
    else:
        form = BookForm(instance=book)
    return render(request, 'books/edit.html', {'form': form})


@permission_required('common.view_books_remove_book', raise_exception=True)
def remove_book(request, book_ids):
    book_list = BookType.objects.filter(pk__in=book_ids.split(','))
    if len(book_list) == 0:
        raise Http404

    if request.method == 'POST':
        set_success_msg(request, 'book_removed' if len(book_list) == 1 else 'books_removed')
        book_list.delete()
        return HttpResponseRedirect(reverse(index))
    else:
        return render(request, 'books/remove.html', {'book_list': book_list})


@permission_required('common.view_books_book_details', raise_exception=True)
def book_details(request, book_id):
    book = get_object_or_404(BookType, id=book_id)
    book.categories_str = ", ".join([category.name for category in book.categories.all()])
    return render(request, 'books/details.html', {'book': book})


def bulk_actions(request, action_name):
    book_list = []
    if action_name == 'remove' and request.method == 'POST':
        for key, value in request.POST.items():
            if value == 'on':
                # Form field names are in format "select-id", so key[7:] will leave us id
                book_list.append(key[7:])
        if book_list:
            return HttpResponseRedirect(reverse(remove_book, args=[",".join(book_list)]))
        else:
            return HttpResponseRedirect(reverse(index))
    else:
        raise Http404
