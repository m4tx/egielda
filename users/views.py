# This file is part of e-Giełda.
# Copyright (C) 2014  Mateusz Maćkowski and Tomasz Zieliński
#
# e-Giełda is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# You should have received a copy of the GNU Affero General Public License
# along with e-Giełda.  If not, see <http://www.gnu.org/licenses/>.

from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from authentication.forms import UserDataForm
from authentication.models import AppUser
from books.models import Book
from orders.models import Order
from utils.alerts import set_success_msg


@permission_required('common.view_users_index', raise_exception=True)
def index(request):
    return HttpResponseRedirect(reverse(verified))


@permission_required('common.view_users_verified', raise_exception=True)
def verified(request):
    users = AppUser.objects.all().order_by('last_name', 'first_name')
    users = [user for user in users if user.verified]
    users = filter(lambda user: user.verified, users)

    return render(request, 'users/users.html', {'users': users})


@permission_required('common.view_users_profile', raise_exception=True)
def profile(request, user_pk):
    user = get_object_or_404(AppUser, id=user_pk)

    disabled_fields_post = ['password']
    disabled_fields_files = ['document']

    if request.POST:
        for field in disabled_fields_post:
            request.POST[field] = getattr(user, field)
        for field in disabled_fields_files:
            request.FILES[field] = getattr(user, field)
        form = UserDataForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            set_success_msg(request, 'user_profile_saved')
            return HttpResponseRedirect(reverse(verified))
    else:
        form = UserDataForm(instance=user)

    for field in disabled_fields_post + disabled_fields_files:
        form.fields[field].widget.attrs['readonly'] = True
        form.fields[field].widget.attrs['disabled'] = True

    del form.fields['password']

    return render(request, 'users/user_profile.html', {'form': form, 'student': user})


@permission_required('common.view_users_profile_purchased', raise_exception=True)
def profile_purchased(request, user_pk):
    user = get_object_or_404(AppUser, id=user_pk)
    orders = Order.objects.filter(user=user).prefetch_related(
        'user', 'orderedbook_set', 'orderedbook_set__book_type').annotate(
        books_count=Sum('orderedbook__count'))

    stats = dict()
    for order in orders:
        order_id = order.date.strftime("%Y%m%d") + "-" + str(order.pk) + "-" + str(
            order.user.pk) + "-" + str(
            order.books_count)

        order_book_list = []
        for orderedbook in order.orderedbook_set.all():
            order_book_list.append((orderedbook.book_type, orderedbook.count, order.fulfilled))

        stats[(order.user.get_full_name(), order_id)] = order_book_list

    return render(request, 'users/purchased.html', {'stats': stats, 'student': user})


@permission_required('common.view_users_profile_sold', raise_exception=True)
def profile_sold(request, user_pk):
    user = get_object_or_404(AppUser, id=user_pk)
    books = Book.objects.filter(owner=user).select_related("book_type")

    stats = dict()  # Dictionary indexed with the book type string, valued with the list containing 4 values: a book
    # itself, amount of books declared to bring, books actually brought and books already sold
    for book in books:
        stats[str(book.book_type)] = stats.setdefault(str(book.book_type), [book, 0, 0, 0])
        stats[str(book.book_type)][1] += 1
        stats[str(book.book_type)][2] += 1 if book.accepted else 0
        stats[str(book.book_type)][3] += 1 if book.sold else 0

    return render(request, 'users/sold.html', {'stats': stats, 'student': user})
