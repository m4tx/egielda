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

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, ContentType, PermissionsMixin
from django.utils.translation import ugettext as _


class AppUserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, student_class, phone_number, email, password):

        if not username or not password:
            raise ValueError('Users must have a username and a password')

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            student_class=student_class,
            phone_number=phone_number,
            email=AppUserManager.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, student_class, phone_number, email, password):
        u = self.create_user(username, first_name, last_name, student_class, phone_number, email, password)
        u.awaiting_verification = False
        u.verified = True
        u.is_superuser = True
        group = Group.objects.get(name='sysadmin')
        u.groups.add(group)
        u.save(using=self._db)
        return u

def new_document_filename(instance, filename):
    return '_'.join([instance.username, instance.first_name, instance.last_name, instance.student_class]) + '.' + \
        filename.split('.')[-1]

class AppUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    student_class = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=9)
    email = models.CharField(max_length=100)
    document = models.ImageField(upload_to=new_document_filename, blank=True)
    awaiting_verification = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'student_class', 'phone_number', 'email']

    objects = AppUserManager()

    @property
    def is_staff(self):
        return self.groups.filter(name='sysadmin').exists()

    def user_name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return _("%(first_name)s %(last_name)s, %(student_class)s" %
                 {'first_name': self.first_name, 'last_name': self.last_name, 'student_class': self.student_class})

    def get_short_name(self):
        return str(self)

    def get_full_name(self):
        return str(self)
