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

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, ContentType, PermissionsMixin
from django.utils.functional import cached_property
from django.utils.translation import ugettext as _
from django.db.models import Q


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
        group = Group.objects.get(name='user')
        user.groups.add(group)
        user.save()
        return user

    def create_superuser(self, username, first_name, last_name, student_class, phone_number, email, password):
        u = self.create_user(username, first_name, last_name, student_class, phone_number, email, password)
        u.awaiting_verification = False
        u.is_superuser = True
        u.groups.add(Group.objects.get(name='sysadmin'))
        u.save(using=self._db)
        return u


def new_document_filename(instance, filename):
    return '_'.join([instance.username, instance.first_name, instance.last_name, instance.student_class]) + '.' + \
        filename.split('.')[-1]


class AppUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True,
                                error_messages={'unique': _("This username already does exist in the database.")})
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    student_class = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=9)
    email = models.CharField(max_length=100)
    document = models.ImageField(upload_to=new_document_filename, blank=True)
    awaiting_verification = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'student_class', 'phone_number', 'email']

    objects = AppUserManager()

    @cached_property
    def is_staff(self):
        return self.groups.filter(name='sysadmin').exists()

    @cached_property
    def verified(self):
        query = Q()
        for group_name in AppUser.get_verified_groups():
            query |= Q(name=group_name)
        return self.groups.filter(query).exists()

    @staticmethod
    def get_verified_groups():
        return ['verified_user', 'moderator', 'admin', 'sysadmin']

    def user_name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return _("%(first_name)s %(last_name)s, %(student_class)s") % {
            'first_name': self.first_name, 'last_name': self.last_name, 'student_class': self.student_class
        }

    def get_short_name(self):
        return _("%(first_name)s %(last_name)s") % {
            'first_name': self.first_name,
            'last_name': self.last_name,
        }

    def get_full_name(self):
        return _("%(first_name)s %(last_name)s, %(student_class)s, %(phone_number)s, %(email)s") % {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'student_class': self.student_class,
            'phone_number': self.phone_number,
            'email': self.email
        }


class AppUserIncorrectFields(models.Model):
    user = models.OneToOneField(AppUser)
    incorrect_fields = models.TextField()
