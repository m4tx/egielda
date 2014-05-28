from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext as _

from books.forms import BookForm
from shared.models import BookType


def index(request):
    book_list = BookType.objects.all()
    args = {'book_list': book_list}
    if 'success_msg' in request.session:
        args['success_msg'] = {
            'book_added': _("The book was added successfully."),
            'book_removed': _("The book was removed successfully."),
            'books_removed': _("The books were removed successfully."),
        }[request.session['success_msg']]
        del request.session['success_msg']
    return render(request, 'books/index.html', args)


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book_type = BookType(publisher=form.cleaned_data['publisher'], title=form.cleaned_data['title'],
                                 edition=form.cleaned_data['edition'],
                                 publication_year=form.cleaned_data['publication_year'],
                                 price=form.cleaned_data['price'] * 100)
            book_type.save()
            request.session['success_msg'] = 'book_added'
            return HttpResponseRedirect(reverse('index'))
    else:
        form = BookForm()
        return render(request, 'books/add.html', {'form': form})


def edit_book(request, book_id):
    return HttpResponse("Hello world!")


def remove_book(request, book_ids):
    book_list = BookType.objects.filter(id__in=book_ids.split(','))
    if request.method == 'POST':
        request.session['success_msg'] = 'book_removed' if len(book_list) == 1 else 'books_removed'
        book_list.delete()
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'books/remove.html', {'book_list': book_list})
