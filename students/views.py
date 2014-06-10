from django.http import HttpResponse
from django.shortcuts import render
from common.models import Student


def index(request):
    student_list = Student.objects.all()
    return render(request, 'students/index.html', {'student_list': student_list})


def unaccepted(request):
    student_list = Student.objects.all()
    return render(request, 'students/unaccepted.html', {'student_list': student_list})


def list_books(request, student_pk):
    return HttpResponse(student_pk)


def accept_books(request, student_pk):
    return HttpResponse(student_pk)