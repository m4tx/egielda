from django.core.urlresolvers import reverse
from django.forms import model_to_dict
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from common.models import Student

from sell.forms import PersonalDataForm


def index(request):
    return HttpResponseRedirect(reverse('sell.views.personal_data'))


def personal_data(request):
    if request.method == 'POST':
        form = PersonalDataForm(request.POST)
        if form.is_valid():
            request.session['personal_data'] = model_to_dict(form.save(commit=False))
            return HttpResponseRedirect(reverse('sell.views.books'))
    else:
        if request.session['personal_data']:
            form = PersonalDataForm(instance=Student(**request.session['personal_data']))
        else:
            form = PersonalDataForm()
    return render(request, 'sell/personal_data.html', {'form': form})


def books(request):
    return HttpResponse("Hello, world!")