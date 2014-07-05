from django.contrib.auth.decorators import user_passes_test

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404

from books.models import BookType

from categories.forms import CategoryForm
from categories.models import Category
from common.auth import user_is_admin
from common.uiutils import alerts


@user_passes_test(user_is_admin)
def index(request):
    book_list = BookType.objects.all()
    category_list = Category.objects.all()
    count = {o: 0 for o in category_list}
    for book in book_list:
        for category in book.categories.all():
            if category is not None:
                count[category] += 1

    return render(request, 'categories/index.html',
                  alerts(request, {'category_list': sorted(count.items(), key=lambda o: o[0].name)}))


@user_passes_test(user_is_admin)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['success_msg'] = 'category_added'
            return HttpResponseRedirect(reverse(index))
    else:
        form = CategoryForm()
    return render(request, 'categories/add.html', {'form': form})


@user_passes_test(user_is_admin)
def edit_category(request, cat_pk):
    category = get_object_or_404(Category, pk=cat_pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            request.session['success_msg'] = 'category_edited'
            return HttpResponseRedirect(reverse(index))
    else:
        form = CategoryForm(instance=category)
    return render(request, 'categories/edit.html', {'form': form})


@user_passes_test(user_is_admin)
def remove_category(request, cat_pk):
    category = get_object_or_404(Category, pk=cat_pk)
    if request.method == 'POST':
        pass
    else:
        book_count = BookType.objects.filter(categories=category).count()
        return render(request, 'categories/remove.html', {'category': category, 'book_count': book_count})


def list_books(request, cat_pk):
    category = get_object_or_404(Category, pk=cat_pk)
    book_list = get_list_or_404(BookType, categories=category)
    return render(request, 'categories/list.html', {'category': category, 'book_list': book_list})