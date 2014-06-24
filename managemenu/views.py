from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from common.auth import user_is_admin


@user_passes_test(user_is_admin)
def index(request):
    return render(request, 'managemenu/index.html')