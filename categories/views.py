from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse

from common.auth import user_is_admin


@user_passes_test(user_is_admin)
def index(request):
    return HttpResponse("Hello, world!")


@user_passes_test(user_is_admin)
def add_category(request):
    return HttpResponse("Hello, world!")


@user_passes_test(user_is_admin)
def edit_category(request):
    return HttpResponse("Hello, world!")


@user_passes_test(user_is_admin)
def remove_category(request):
    return HttpResponse("Hello, world!")