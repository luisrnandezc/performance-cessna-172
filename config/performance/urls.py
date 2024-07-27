from django.urls import path

from . import views

app_name = 'performance'

urlpatterns = [
    path("", views.data_input, name="input"),
]