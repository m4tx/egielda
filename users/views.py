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

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.db.models import Sum, Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext as _

from authentication.forms import UserDataForm
from authentication.models import AppUser, AppUserHasCorrectData
from books.models import Book
from orders.models import Order
from utils.alerts import set_success_msg
from authentication.signals import user_verified


@permission_required('common.view_users_index', raise_exception=True)
def index(request):
    return HttpResponseRedirect(reverse(verified))


@permission_required('common.view_users_verified', raise_exception=True)
def verified(request):
    users = AppUser.objects.filter(groups__name__in=AppUser.get_verified_groups()).order_by('last_name', 'first_name')

    return render(request, 'users/users.html', {'users': users, 'tab': 'verified'})


@permission_required('common.view_users_unverified', raise_exception=True)
def unverified(request):
    users = AppUser.objects.exclude(groups__name__in=AppUser.get_verified_groups()).order_by('last_name', 'first_name')

    return render(request, 'users/users.html', {'users': users, 'tab': 'unverified'})


@permission_required('common.view_users_verify', raise_exception=True)
def verify(request, user_pk):
    student = get_object_or_404(AppUser,
                                Q(pk=user_pk) & ~Q(groups__name__in=AppUser.get_verified_groups()))
    if request.POST:
        group = Group.objects.get(name='verified_user')
        student.groups.add(group)
        student.awaiting_verification = False
        student.save()

        AppUserHasCorrectData.objects.filter(user=user_pk).delete()

        user_verified.send(sender=None, user=student)
        set_success_msg(request, 'user_verified')

        return HttpResponseRedirect(reverse(unverified))
    else:
        return render(request, 'users/verify.html', {'student': student})


@permission_required('common.view_users_verify', raise_exception=True)
def needs_correction(request, user_pk):
    if request.method == 'POST':
        user = get_object_or_404(AppUser, Q(pk=user_pk) & ~Q(groups__name__in=AppUser.get_verified_groups()))
        user.awaiting_verification = False
        user.save()
        incorrect_fields = request.POST['incorrect_fields'].split(',')

        fields_to_save = []
        for incorrect_field in incorrect_fields:
            for field in AppUser._meta.local_fields:
                if field.name == incorrect_field:
                    fields_to_save.append((field.name, _(field.verbose_name.capitalize())))

        has_correct_data = AppUserHasCorrectData.objects.get_or_create(user=user)[0]
        has_correct_data.incorrect_fields = json.dumps(fields_to_save)
        has_correct_data.save()

        set_success_msg(request, 'incorrect_fields_saved')

        return HttpResponseRedirect(reverse(unverified))
    else:
        raise Http404


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
