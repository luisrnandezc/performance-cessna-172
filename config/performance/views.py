# Imports.
import sys
import os
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import PerformanceData

# Add the path to the scripts directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from src import run_performance


# App views.
def data_input(request):
    if request.method == "POST":
        form = PerformanceData(request.POST)
        if form.is_valid():
            request.session["output_data"] = run_performance.compute_performance(form.cleaned_data)
            return HttpResponseRedirect("output")
    else:
        form = PerformanceData()
    return render(request, "performance/input.html", {"form": form})


def data_output(request):
    performance_data = request.session["output_data"]
    return render(request, "performance/output.html", {'performance_data': performance_data})
