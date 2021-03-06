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
from django.contrib import messages

from django.core.urlresolvers import reverse
from django.db.models import Sum, Q
from django.http import HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext as _

from authentication.decorators import permission_required
from authentication.forms import UserDataForm
from authentication.models import AppUser, AppUserIncorrectFields
from books.models import Book
from orders.models import Order
from authentication.signals import user_needs_correction


@permission_required('common.view_users_index')
def index(request):
    return HttpResponseRedirect(reverse(verified))


@permission_required('common.view_users_verified')
def verified(request):
    users = AppUser.objects.filter(groups__name__in=AppUser.get_verified_groups()).order_by('last_name', 'first_name')

    return render(request, 'users/users.html', {'users': users, 'tab': 'verified'})


@permission_required('common.view_users_unverified')
def unverified(request):
    needing_correction = AppUserIncorrectFields.objects.all().values_list('user_id')
    users = (AppUser.objects
             .exclude(id__in=needing_correction)
             .exclude(groups__name__in=AppUser.get_verified_groups())
             .order_by('last_name', 'first_name'))

    return render(request, 'users/users.html', {'users': users, 'tab': 'unverified'})


@permission_required('common.view_users_needing_data_correction')
def needing_data_correction(request):
    users_qs = (AppUserIncorrectFields.objects.select_related('user')
                .exclude(user__groups__name__in=AppUser.get_verified_groups())
                .order_by('user__last_name', 'user__first_name'))
    users = [x.user for x in users_qs]
    return render(request, 'users/users.html', {'users': users, 'tab': 'needing_data_correction'})


@permission_required('common.view_users_verify')
def verify(request, user_pk):
    student = get_object_or_404(AppUser,
                                Q(pk=user_pk) & ~Q(groups__name__in=AppUser.get_verified_groups()))
    if request.POST:
        student.verify()
        messages.success(request, _("User was verified successfully."))
        return HttpResponseRedirect(reverse(unverified))
    else:
        return render(request, 'users/verify.html', {'student': student})


@permission_required('common.view_users_verify')
def needs_correction(request, user_pk):
    if request.method == 'POST':
        if len(request.POST.get('incorrect_fields', '')) == 0:
            return HttpResponseBadRequest()

        user = get_object_or_404(AppUser, Q(pk=user_pk) & ~Q(groups__name__in=AppUser.get_verified_groups()))
        user.awaiting_verification = False
        user.save()
        incorrect_fields = request.POST['incorrect_fields'].split(',')

        fields_to_save = []
        for incorrect_field in incorrect_fields:
            for field in AppUser._meta.local_fields:
                if field.name == incorrect_field:
                    fields_to_save.append((field.name, _(field.verbose_name.capitalize())))

        has_correct_data = AppUserIncorrectFields.objects.get_or_create(user=user)[0]
        has_correct_data.incorrect_fields = json.dumps(fields_to_save)
        has_correct_data.save()

        user_needs_correction.send(sender=None, user=user, incorrect_fields=fields_to_save)
        messages.success(request, _("Information about incorrect data was sent to user."))

        return HttpResponseRedirect(reverse(unverified))
    else:
        raise Http404


@permission_required('common.view_users_profile')
def profile(request, user_pk):
    user = get_object_or_404(AppUser, id=user_pk)

    disabled_fields_post = ['password', 'retype_password']
    disabled_fields_files = ['document']

    if request.POST:
        for field in disabled_fields_post:
            if field == 'retype_password':
                request.POST[field] = user.password
            else:
                request.POST[field] = getattr(user, field)
        for field in disabled_fields_files:
            request.FILES[field] = getattr(user, field)
        form = UserDataForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, _("User's profile data was successfully updated."))
            return HttpResponseRedirect(reverse(verified))
    else:
        form = UserDataForm(instance=user)

    for field in disabled_fields_post + disabled_fields_files:
        form.fields[field].widget.attrs['readonly'] = True
        form.fields[field].widget.attrs['disabled'] = True

    del form.fields['password']
    del form.fields['retype_password']

    return render(request, 'users/user_profile.html', {'form': form, 'student': user})


@permission_required('common.view_users_profile_purchased')
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


@permission_required('common.view_users_profile_sold')
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
