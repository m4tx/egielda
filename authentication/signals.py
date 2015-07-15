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

from django.core.mail import mail_admins
from django.db.models.signals import post_init, post_save
from django.dispatch import receiver

from django.utils.translation import ugettext as _

from authentication.models import AppUser
from egielda import settings


@receiver(post_init, sender=AppUser)
def awaiting_verification_init(sender, instance, **kwargs):
    instance.__original_awaiting_verification = instance.awaiting_verification


@receiver(post_save, sender=AppUser)
def awaiting_verification_save(sender, instance, **kwargs):
    if (instance.awaiting_verification != instance.__original_awaiting_verification and
            instance.awaiting_verification):
        # Send email to admins that there's new user awaiting verification
        params = {
            'username': instance,
            'site_name': getattr(settings, 'SITE_NAME', "e-Giełda"),
        }
        subject = _("{username} on {site_name} is awaiting verification").format(**params)
        message = _("""Hello,

{username} on {site_name} is awaiting verification.""").format(**params)
        mail_admins(subject, message, fail_silently=True)
