from django.shortcuts import render

from sell.forms import PersonalDataForm


def index(request):
    if request.method == 'POST':
        pass
    else:
        form = PersonalDataForm()
    return render(request, 'sell/personal_data.html', {'form': form})