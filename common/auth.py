from django.contrib.auth.models import User


def user_is_admin(user: User):
    return user.is_authenticated() and user.is_staff