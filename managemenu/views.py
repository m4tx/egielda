from django.contrib.auth.decorators import permission_required
from django.shortcuts import render


@permission_required('common.view_managemenu_index', raise_exception=True)
def index(request):
    return render(request, 'managemenu/index.html')