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

from django.contrib import messages
from django.utils.translation import ugettext as _

from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, HttpResponseNotAllowed
from django.contrib.auth.models import Group

from django.db.models import Sum

from authentication.decorators import permission_required
from authentication.forms import UserDataForm, SupplementForm, RegistrationForm
from books.models import Book
from egielda import settings
from settings.settings import Settings
from utils.ldap import check_user_existence
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
            user.save()

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


@permission_required('common.view_authentication_profile')
def profile(request):
    disabled_fields_post = ['username', 'password']
    disabled_fields_files = []

    if request.user.verified:
        disabled_fields_post += ['first_name', 'last_name', 'year', 'class_letter']
        disabled_fields_files += ['document']

    if request.POST:
        for field in disabled_fields_post:
            request.POST[field] = getattr(request.user, field)
        for field in disabled_fields_files:
            request.FILES[field] = getattr(request.user, field)

        # document can't be removed by just not sending a file, in which case we set the previous value stored in db
        if request.user.document and 'document' not in request.FILES and 'document-clear' not in request.POST:
            request.FILES['document'] = request.user.document

        form = UserDataForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            user = form.save()

            if settings.USE_LDAP_VERIFICATION and user.verified is False and check_user_existence(user):
                user.verify()
            else:
                if 'document' in request.FILES and user.awaiting_verification is False and user.verified is False:
                    user.awaiting_verification = True
                    AppUserIncorrectFields.objects.filter(user=user).delete()
                elif 'document-clear' in request.POST and user.awaiting_verification is True:
                    user.awaiting_verification = False
                user.save()
            messages.success(request, _("Your profile data was successfully updated."))
            return HttpResponseRedirect(reverse(profile))

    else:
        form = UserDataForm(instance=request.user)
        form.cleaned_data = {}

        for field in request.user.incorrect_fields:
            form.add_error(field[0], '')

    for field in disabled_fields_post + disabled_fields_files:
        form.fields[field].widget.attrs['readonly'] = True
        form.fields[field].widget.attrs['disabled'] = True

    del form.fields['password']

    return render(request, 'authentication/profile.html', {'form': form})


@permission_required('common.view_authentication_profile_purchased')
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


@permission_required('common.view_authentication_profile_sold')
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
