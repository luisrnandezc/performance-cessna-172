# Imports.
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .src import run_weight_balance
from .forms import CSVFileForm
from .forms import ManualForm
from .models import CSVFile, UploadCSVData
import csv
import io


def data_input(request):
    file_form = CSVFileForm
    manual_form = ManualForm
    if request.method == 'POST':
        if 'submit_file_form' in request.POST:
            file_form = CSVFileForm(request.POST, request.FILES)
            if file_form.is_valid():
                csv_file = file_form.cleaned_data
                data = process_csv(csv_file)
                request.session["output_data"] = run_weight_balance.compute_weight_and_balance(data)
                return HttpResponseRedirect("output")
        elif 'submit_manual_form' in request.POST:
            manual_form = ManualForm(request.POST)
            if manual_form.is_valid():
                data = manual_form.cleaned_data
                request.session["output_data"] = run_weight_balance.compute_weight_and_balance(data)
                return HttpResponseRedirect("output")
    return render(request, "weight_balance/input.html", {'file_form': file_form, 'manual_form': manual_form})


def data_output(request):
    weight_balance_data = request.session["output_data"]
    return render(request, "weight_balance/output.html", {'weight_balance_data': weight_balance_data})


def process_csv(csv_file):
    file = csv_file['csv_file'].open(mode='r')
    data_set = file.read()
    io_string = io.StringIO(data_set.decode("utf-8"))
    csv_reader = csv.reader(io_string, delimiter=',')
    weight_data = {}
    fields = ['seat_config', 'basic_weight', 'basic_moment',
              'usable_fuel', 'pilot', 'front_pax', 'rear_pax_1', 'rear_pax_2', 'cargo_1', 'cargo_2', 'fuel_allowance']
    for (field, row) in zip(fields, csv_reader):
        value = row[1]
        if value.isnumeric() or value[0] == '-':
            weight_data[field] = int(value)
        else:
            weight_data[field] = value

    return weight_data
