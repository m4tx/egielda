from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_list_or_404
from django.utils.translation import ugettext as _

from books.forms import BookForm
from common.models import BookType


def index(request):
    book_list = BookType.objects.all()
    args = {'book_list': book_list}
    if 'success_msg' in request.session:
        args['success_msg'] = {
            'book_added': _("The book was added successfully."),
            'book_edited': _("The book was edited successfully."),
            'book_removed': _("The book was removed successfully."),
            'books_removed': _("The books were removed successfully."),
        }[request.session['success_msg']]
        del request.session['success_msg']
    return render(request, 'books/index.html', args)


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['success_msg'] = 'book_added'
            return HttpResponseRedirect(reverse('index'))
    else:
        form = BookForm()
    return render(request, 'books/add.html', {'form': form})


def edit_book(request, book_id):
    book = BookType.objects.get(id=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            request.session['success_msg'] = 'book_edited'
            return HttpResponseRedirect(reverse('index'))
    else:
        form = BookForm(instance=book)
    return render(request, 'books/edit.html', {'form': form})


def remove_book(request, book_ids):
    book_list = get_list_or_404(BookType, id__in=book_ids.split(','))
    if request.method == 'POST':
        request.session['success_msg'] = 'book_removed' if len(book_list) == 1 else 'books_removed'
        book_list.delete()
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'books/remove.html', {'book_list': book_list})
