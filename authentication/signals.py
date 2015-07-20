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

from urllib.parse import urljoin

from django.core.mail import mail_admins, send_mail
from django.core.urlresolvers import reverse
from django.db.models.signals import post_init, post_save
from django.dispatch import receiver, Signal

from django.utils.translation import ugettext as _

from authentication.models import AppUser
from django.conf import settings


user_verified = Signal(providing_args=['user'])
user_needs_correction = Signal(providing_args=['user', 'incorrect_fields'])


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
            'verification_url': urljoin(settings.CURRENT_URL,
                                        reverse('users.views.verify', args=[instance.pk]))
        }
        subject = _("{username} on {site_name} is awaiting verification").format(**params)
        message = (_("""Hello,

{username} on {site_name} is awaiting verification. To verify them, visit {verification_url}""")
                   .format(**params))
        html_message = (_("Hello,"
                          "<p>{username} on {site_name} is awaiting verification."
                          "<p><a href='{verification_url}'>Verify {username}</a>")
                        .format(**params))
        mail_admins(subject, message, fail_silently=True, html_message=html_message)


@receiver(user_verified)
def send_mail_to_verified_user(sender, user, **kwargs):
    params = {
        'site_name': getattr(settings, 'SITE_NAME', "e-Giełda"),
        'username': user.get_short_name(),
    }
    subject = _("[{site_name}] Your account was successfully verified").format(**params)
    message = (_("""Hello {username},

Your account was successfully verified. You will be able to sell and purchase books within specified time span.""")
               .format(**params))
    html_message = (_("Hello {username},"
                      "<p>Your account was successfully verified. You will be able to sell and purchase books "
                      "within specified time span.")
                    .format(**params))

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True,
              html_message=html_message)


@receiver(user_needs_correction)
def send_mail_to_unverified_user(sender, user, incorrect_fields, **kwargs):
    params = {
        'site_name': getattr(settings, 'SITE_NAME', "e-Giełda"),
        'username': user.get_short_name(),
    }
    subject = _("[{site_name}] Your profile data needs correction").format(**params)
    message = (_("""Hello {username},

The data you provided in your profile was found incorrect. Following fields don't match a scan of your identity \
card or contain other errors:
""").format(**params))

    for field in incorrect_fields:
        message += "- " + field[1] + "\n"

    message += _("In order to get your account verified, you will need to correct them.")

    html_message = (_("Hello {username},"
                      "<p>The data you provided in your profile was found incorrect. Following fields "
                      "don't match a scan of your identity card or contain other errors:")
                    .format(**params))

    html_message += "<ul>"
    for field in incorrect_fields:
        html_message += "<li>" + field[1] + "</li>"
    html_message += "</ul>"

    html_message += _("<p>In order to get your account verified, you will need to correct them.")

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True,
              html_message=html_message)
