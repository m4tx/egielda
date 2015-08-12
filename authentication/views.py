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

import json

from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, HttpResponseNotAllowed
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from django.db.models import Sum

from authentication.forms import UserDataForm, SupplementForm, RegistrationForm
from books.models import Book
from egielda import settings
from settings.settings import Settings
from utils.LDAP import check_user_existence
from utils.alerts import set_success_msg
from orders.models import Order
from authentication.models import AppUserIncorrectFields, AppUser


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            group = Group.objects.get(name='user')
            user.groups.add(group)

            if settings.USE_LDAP_VERIFICATION:
                if check_user_existence(user):
                    user.verify()
                else:
                    request.session['user_to_supplement'] = user.pk
                    return render(request, 'authentication/registration_unverified.html', {'form': SupplementForm()})
            else:
                if 'document' in request.FILES:
                    user.awaiting_verification = True
            user.save()
            return render(request, 'authentication/registration_complete.html', {'verified': user.verified})
    else:
        form = RegistrationForm()

    return render(request, 'authentication/register.html',
                  {'form': form, 'tos_url': getattr(Settings('tos_url'), 'tos_url', None),
                   'use_LDAP_verification': settings.USE_LDAP_VERIFICATION})


def register_supplement(request):
    if request.method == 'POST' and 'user_to_supplement' in request.session:
        user = get_object_or_404(AppUser, pk=request.session['user_to_supplement'])
        del request.session['user_to_supplement']
        form = SupplementForm(request.POST, request.FILES)
        if form.is_valid():
            if 'document' in request.FILES:
                user.document = form.cleaned_data['document']
                user.awaiting_verification = True
                user.save()

            return render(request, 'authentication/registration_complete.html', {'verified': False})
        else:
            return render(request, 'authentication/registration_unverified.html', {'form': form})

    else:
        return HttpResponseNotAllowed(['POST'])


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
            if 'document' in form.cleaned_data and user.awaiting_verification is False:
                user.awaiting_verification = True
                AppUserIncorrectFields.objects.filter(user=user).delete()
            elif 'document-clear' in request.POST and user.awaiting_verification is True:
                user.awaiting_verification = False
            user.save()
            set_success_msg(request, 'profile_saved')
            return HttpResponseRedirect(reverse(profile))
        else:
            incorrect_fields = None
    else:
        form = UserDataForm(instance=request.user)
        form.cleaned_data = {}
        incorrect_fields = None
        try:
            incorrect_fields = AppUserIncorrectFields.objects.get(user=request.user).incorrect_fields
            incorrect_fields = json.loads(incorrect_fields)
            for field in incorrect_fields:
                form.add_error(field[0], '')
        except AppUserIncorrectFields.DoesNotExist:
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
