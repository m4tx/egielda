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
import json

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from django.db.models import Sum

from authentication.forms import UserDataForm
from books.models import Book
from utils.alerts import set_success_msg
from orders.models import Order
from authentication.models import AppUserHasCorrectData


def register(request):
    if request.method == 'POST':
        form = UserDataForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            if 'document' in request.FILES:
                user.awaiting_verification = True
            user.set_password(user.password)
            group = Group.objects.get(name='user')
            user.groups.add(group)
            user.save()
            return render(request, 'authentication/registration_complete.html', {})
    else:
        form = UserDataForm()

    return render(request, 'authentication/register.html', {'form': form})


@permission_required('common.view_authentication_profile', raise_exception=True)
def profile(request):
    disabled_fields_post = ['username', 'password']
    disabled_fields_files = []

    if request.user.verified:
        disabled_fields_post += ['first_name', 'last_name', 'student_class']
        disabled_fields_files += ['document']

    if request.POST:
        for field in disabled_fields_post:
            request.POST[field] = getattr(request.user, field)
        for field in disabled_fields_files:
            request.FILES[field] = getattr(request.user, field)
        form = UserDataForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            user = form.save()
            if 'document' in request.FILES and user.awaiting_verification is False:
                user.awaiting_verification = True
            elif 'document' not in request.FILES and user.awaiting_verification is True:
                user.awaiting_verification = False
            user.save()
            set_success_msg(request, 'profile_saved')
            return HttpResponseRedirect(reverse(profile))
    else:
        form = UserDataForm(instance=request.user)
        #form.is_bound = True
        form.cleaned_data = {}
        if form.is_valid():
            print(form.cleaned_data)
        else:
            print(form.is_bound)
            print(form.errors)
        incorrect_fields = None
        try:
            incorrect_fields = AppUserHasCorrectData.objects.get(user=request.user).incorrect_fields
            incorrect_fields = json.loads(incorrect_fields)
            for field in incorrect_fields:
                form.add_error(field[0], '')
        except AppUserHasCorrectData.DoesNotExist:
            pass

    for field in disabled_fields_post + disabled_fields_files:
        form.fields[field].widget.attrs['readonly'] = True
        form.fields[field].widget.attrs['disabled'] = True

    del form.fields['password']

    return render(request, 'authentication/profile.html', {'form': form, 'incorrect_fields': incorrect_fields})


@permission_required('common.view_authentication_profile_purchased', raise_exception=True)
def purchased(request):
    orders = Order.objects.filter(user=request.user).prefetch_related(
        'user', 'orderedbook_set', 'orderedbook_set__book_type').annotate(books_count=Sum('orderedbook__count'))

    stats = dict()
    for order in orders:
        order_id = order.date.strftime("%Y%m%d") + "-" + str(order.pk) + "-" + str(order.user.pk) + "-" + str(
            order.books_count)

        order_book_list = []
        for orderedbook in order.orderedbook_set.all():
            order_book_list.append((orderedbook.book_type, orderedbook.count, order.fulfilled))

        stats[(order.user.get_full_name(), order_id)] = order_book_list

    return render(request, 'authentication/purchased.html', {'stats': stats})


@permission_required('common.view_authentication_profile_sold', raise_exception=True)
def sold(request):
    books = Book.objects.filter(owner=request.user).select_related("book_type")

    stats = dict()  # Dictionary indexed with the book type string, valued with the list containing 4 values: a book
                    # itself, amount of books declared to bring, books actually brought and books already sold
    for book in books:
        stats[str(book.book_type)] = stats.setdefault(str(book.book_type), [book, 0, 0, 0])
        stats[str(book.book_type)][1] += 1
        stats[str(book.book_type)][2] += 1 if book.accepted else 0
        stats[str(book.book_type)][3] += 1 if book.sold else 0

    return render(request, 'authentication/sold.html', {'stats': stats})
