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

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404

from authentication.decorators import permission_required
from books.models import BookType
from categories.forms import CategoryForm
from categories.models import Category
from utils.alerts import set_success_msg


@permission_required('common.view_categories_index')
def index(request):
    book_list = BookType.objects.all().prefetch_related('categories')
    category_list = Category.objects.all()
    count = {o: 0 for o in category_list}
    for book in book_list:
        for category in book.categories.all():
            if category is not None:
                count[category] += 1

    return render(request, 'categories/index.html', {'category_list': sorted(count.items(), key=lambda o: o[0].name)})


@permission_required('common.view_categories_add_category')
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            set_success_msg(request, 'category_added')
            return HttpResponseRedirect(reverse(index))
    else:
        form = CategoryForm()
    return render(request, 'categories/add.html', {'form': form})


@permission_required('common.view_categories_edit_category')
def edit_category(request, cat_pk):
    category = get_object_or_404(Category, pk=cat_pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            set_success_msg(request, 'category_edited')
            return HttpResponseRedirect(reverse(index))
    else:
        form = CategoryForm(instance=category)
    return render(request, 'categories/edit.html', {'form': form})


@permission_required('common.view_categories_remove_category')
def remove_category(request, cat_pk):
    category = get_object_or_404(Category, pk=cat_pk)
    if request.method == 'POST':
        category.delete()
        set_success_msg(request, 'category_remove')
        return HttpResponseRedirect(reverse(index))
    else:
        book_count = BookType.objects.filter(categories=category).count()
        return render(request, 'categories/remove.html', {'category': category, 'book_count': book_count})


@permission_required('common.view_categories_list_books')
def list_books(request, cat_pk):
    category = get_object_or_404(Category, pk=cat_pk)
    book_list = get_list_or_404(BookType, categories=category)
    return render(request, 'categories/list.html', {'category': category, 'book_list': book_list})
