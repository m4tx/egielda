from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404

from books.forms import BookForm
from common.auth import user_is_admin
from common.models import BookType
from common.uiutils import alerts


@user_passes_test(user_is_admin)
def index(request):
    book_list = BookType.objects.all()
    return render(request, 'books/index.html', alerts(request, {'book_list': book_list}))


@user_passes_test(user_is_admin)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['success_msg'] = 'book_added'
            return HttpResponseRedirect(reverse(index))
    else:
        form = BookForm()
    return render(request, 'books/add.html', {'form': form})


@user_passes_test(user_is_admin)
def edit_book(request, book_id):
    book = get_object_or_404(BookType, id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            request.session['success_msg'] = 'book_edited'
            return HttpResponseRedirect(reverse(index))
    else:
        form = BookForm(instance=book)
    return render(request, 'books/edit.html', {'form': form})


@user_passes_test(user_is_admin)
def remove_book(request, book_ids):
    book_list = get_list_or_404(BookType, id__in=book_ids.split(','))
    if request.method == 'POST':
        request.session['success_msg'] = 'book_removed' if len(book_list) == 1 else 'books_removed'
        book_list.delete()
        return HttpResponseRedirect(reverse(index))
    else:
        return render(request, 'books/remove.html', {'book_list': book_list})


@user_passes_test(user_is_admin)
def bulk_actions(request, action_name):
    book_list = []
    if action_name == 'remove' and request.method == 'POST':
        for item in request.POST.lists():
            if item[1][0] == 'on':
                book_list.append(item[0][7:])
        if book_list:
            return HttpResponseRedirect(reverse(remove_book, args=[",".join(book_list)]))
        else:
            return HttpResponseRedirect(reverse(index))
    else:
        raise Http404