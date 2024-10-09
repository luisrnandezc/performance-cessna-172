# Imports.
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .src import run_performance
from .forms import CSVFileForm
from .forms import ManualForm
from .models import CSVFile, UploadCSVData
import csv
import io
from .validators import *


def data_input(request):
    file_form = CSVFileForm
    manual_form = ManualForm
    if request.method == 'POST':
        if 'submit_file_form' in request.POST:
            file_form = CSVFileForm(request.POST, request.FILES)
            if file_form.is_valid():
                csv_file = file_form.cleaned_data
                data = process_csv(csv_file)
                request.session["output_data"] = run_performance.compute_performance(data)
                return HttpResponseRedirect("output")
        elif 'submit_manual_form' in request.POST:
            manual_form = ManualForm(request.POST)
            if manual_form.is_valid():
                data = manual_form.cleaned_data
                request.session["output_data"] = run_performance.compute_performance(data)
                return HttpResponseRedirect("output")
    return render(request, "performance/input.html", {'file_form': file_form, 'manual_form': manual_form})


def data_output(request):
    performance_data = request.session["output_data"]
    return render(request, "performance/output.html", {'performance_data': performance_data})


def process_csv(csv_file):
    file = csv_file['csv_file'].open(mode='r')
    data_set = file.read()
    io_string = io.StringIO(data_set.decode("utf-8"))
    csv_reader = csv.reader(io_string, delimiter=',')
    performance_data = {}
    fields = ['to_weight', 'fuel_capacity',
              'to_heading', 'to_length', 'to_condition', 'to_press_alt', 'to_temp', 'to_wind_speed', 'to_wind_direction',
              'travel_dist', 'cr_heading', 'cr_press_alt', 'cr_temp', 'cr_wind_speed', 'cr_wind_direction', 'cr_power',
              'land_heading', 'land_length', 'land_condition', 'land_press_alt', 'land_temp', 'land_wind_speed', 'land_wind_direction']
    for (field, row) in zip(fields, csv_reader):
        value = row[1]
        if value.isnumeric():
            performance_data[field] = int(value)
        else:
            performance_data[field] = value

    return performance_data
