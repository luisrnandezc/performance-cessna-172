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
    print("run_performance module:", run_performance)  # Debugging line
    print("Attributes in run_performance:", dir(run_performance))   # Debugging line
    if request.method == "POST":
        form = PerformanceData(request.POST)
        if form.is_valid():
            output_data = run_performance.compute_performance(form.cleaned_data)
            print(output_data)
            return HttpResponseRedirect("output")
    else:
        form = PerformanceData()
    return render(request, "performance/input.html", {"form": form})


def data_output(request):
    return render(request, "performance/output.html")
