from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import PerformanceData


def data_input(request):
    if request.method == "POST":
        form = PerformanceData(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("output")
    else:
        form = PerformanceData()
    return render(request, "performance/input.html", {"form": form})


def data_output(request):
    return render(request, "performance/output.html")
