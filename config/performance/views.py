# Imports.
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ManualForm
from .src import run_performance
from .forms import CSVFileForm
from .models import CSVFile, UploadCSVData
import csv
import io


def data_input(request):
    file_form = CSVFileForm
    manual_form = ManualForm
    if 'submit_file_form' in request.method == 'POST':
        file_form = CSVFileForm(request.POST, request.FILES)
        if file_form.is_valid():
            csv_file = file_form.save()
            process_csv(csv_file)
            request.session["output_data"] = run_performance.compute_performance(file_form.cleaned_data)
    elif 'submit_manual_form' in request.method == "POST":
        manual_form = ManualForm(request.POST)
        if manual_form.is_valid():
            request.session["output_data"] = run_performance.compute_performance(manual_form.cleaned_data)
            return HttpResponseRedirect("output")
    return render(request, "performance/input.html", {'file_form': file_form, 'manual_form': manual_form})


def data_output(request):
    performance_data = request.session["output_data"]
    return render(request, "performance/output.html", {'performance_data': performance_data})


# def upload_csv(request):
#     if request.method == 'POST':
#         form = CSVFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             csv_file = form.save()
#             process_csv(csv_file)
#             return HttpResponseRedirect("output")
#     else:
#         form = CSVFileForm()
#     return render(request, "performance/input.html", {"form": form})


def process_csv(csv_file):
    file = csv_file.file.open(mode='r')
    data_set = file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    csv_reader = csv.reader(io_string, delimiter=',')
    next(csv_reader)
    performance_data = {}
    fields = ['to_weight', 'fuel_capacity'
              'to_heading', 'to_length', 'to_condition', 'to_press_alt', 'to_temp', 'to_wind_speed', 'to_wind_direction',
              'travel_dist', 'cr_heading', 'cr_press_alt', 'cr_temp', 'cr_wind_speed', 'cr_wind_direction', 'cr_power',
              'land_heading', 'land_length', 'land_condition', 'land_press_alt', 'land_temp', 'land_wind_speed', 'land_wind_direction']
    for (field, row) in zip(fields, csv_reader):
        performance_data[field] = row[1]
    if all(field in performance_data for field in fields):
        UploadCSVData.objects.create(
            to_weight=performance_data['to_weight'],
            fuel_capacity=performance_data['fuel_capacity'],
            to_heading=performance_data['to_heading'],
            to_length=performance_data['to_length'],
            to_condition=performance_data['to_condition'],
            to_press_alt=performance_data['to_press_alt'],
            to_temp=performance_data['to_temp'],
            to_wind_speed=performance_data['to_wind_speed'],
            to_wind_direction=performance_data['to_wind_direction'],
            travel_dist=performance_data['travel_dist'],
            cr_heading=performance_data['cr_heading'],
            cr_press_alt=performance_data['cr_press_alt'],
            cr_temp=performance_data['cr_temp'],
            cr_wind_speed=performance_data['cr_wind_speed'],
            cr_wind_direction=performance_data['cr_wind_direction'],
            cr_power=performance_data['cr_power'],
            land_heading=performance_data['land_heading'],
            land_length=performance_data['land_length'],
            land_condition=performance_data['land_condition'],
            land_press_alt=performance_data['land_press_alt'],
            land_temp=performance_data['land_temp'],
            land_wind_speed=performance_data['land_wind_speed'],
            land_wind_direction=performance_data['land_wind_direction']
        )
