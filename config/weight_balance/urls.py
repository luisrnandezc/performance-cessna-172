from django.urls import path
from . import views

app_name = 'weight_balance'

urlpatterns = [
    path("", views.data_input, name="input"),
    path("output", views.data_output, name="output"),
]
