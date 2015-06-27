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

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group

from authentication.forms import UserDataForm
from utils.alerts import set_success_msg

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
    request.user.verified = request.user.groups.filter(name='verified_user').exists()
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

    for field in disabled_fields_post + disabled_fields_files:
        form.fields[field].widget.attrs['readonly'] = True
        form.fields[field].widget.attrs['disabled'] = True

    del form.fields['password']

    return render(request, 'authentication/profile.html', {'form': form, 'user': request.user})
