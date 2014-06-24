from django.contrib.auth.decorators import user_passes_test

from common.auth import user_is_admin


@user_passes_test(user_is_admin)
def index(request):
    pass