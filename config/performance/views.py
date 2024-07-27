from django.shortcuts import render
from django.http import HttpResponse


def data_input(request):
    return render(request, "performance/input.html")
