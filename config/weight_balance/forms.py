from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class CSVFileForm(forms.Form):
    csv_file = forms.FileField(label="Upload CSV file")

    def clean_file(self):
        file = self.cleaned_data['file']
        if file and not file.name.endswith('.csv'):
            raise forms.ValidationError("File type not supported. Please upload a CSV file")
        return file


class ManualForm(forms.Form):
    error_css_class = "error"

    # Radio choices.
    SEAT_CONFIG = [
        (0, 'Standard'),
        (1, 'Optional'),
    ]

    TANK_VOLUME = [
        (40, '40 gal'),
        (50, '50 gal'),
    ]

    # General fields.
    seat_config = forms.TypedChoiceField(widget=forms.RadioSelect, choices=SEAT_CONFIG, coerce=int)
    basic_weight = forms.IntegerField(min_value=1397, max_value=2300,
                                      widget=forms.TextInput(attrs={'placeholder': 'Basic empty weight in lb'}))
    basic_moment = forms.IntegerField(min_value=0, max_value=120,
                                      widget=forms.TextInput(attrs={'placeholder': 'Basic empty moment in lb-in (/1000)'}))
    fuel_capacity = forms.TypedChoiceField(widget=forms.RadioSelect, choices=TANK_VOLUME, coerce=int)

    # Weight data.
    pilot = forms.IntegerField(min_value=0, widget=forms.TextInput(attrs={'placeholder': 'Pilot weight in lb'}))
    front_pax = forms.IntegerField(min_value=0, widget=forms.TextInput(attrs={'placeholder': 'Front pax weight in lb'}))
    rear_pax_1 = forms.IntegerField(min_value=0, widget=forms.TextInput(attrs={'placeholder': 'Rear pax weight in lb'}))
    rear_pax_2 = forms.IntegerField(min_value=0, widget=forms.TextInput(attrs={'placeholder': 'Rear pax weight in lb'}))
    cargo_1 = forms.IntegerField(min_value=0, max_value=120,
                                 widget=forms.TextInput(attrs={'placeholder': 'Baggage area 1 in lb'}))
    cargo_2 = forms.IntegerField(min_value=0, max_value=50,
                                 widget=forms.TextInput(attrs={'placeholder': 'Baggage area 2 in lb'}))
    fuel_allowance = forms.FloatField(min_value=0, widget=forms.TextInput(attrs={'placeholder': 'Fuel allowance in lb'}))

    # General data validation.
    def clean_basic_weight(self):
        data = self.cleaned_data['basic_weight']
        if data < 1397 or data > 2300:
            raise ValidationError(_('Invalid weight - The weight must be between 1397 and 2300 pounds'))
        return data

    # Weight data validation.
    def clean_basic_moment(self):
        data = self.cleaned_data['basic_moment']
        if data < 0 or data > 120:
            raise ValidationError(_('Invalid moment - The moment must be between 0 and 120 lb-in (/1000)'))
        return data

    def clean_pilot(self):
        data = self.cleaned_data['pilot']
        if data < 0 or data > 400:
            raise ValidationError(_('Invalid weight - The weight must be between 0 and 400 pounds'))
        return data

    def clean_front_pax(self):
        data = self.cleaned_data['front_pax']
        if data < 0 or data > 400:
            raise ValidationError(_('Invalid weight - The weight must be between 0 and 400 pounds'))
        return data

    def clean_rear_pax_1(self):
        data = self.cleaned_data['rear_pax_1']
        if data < 0 or data > 400:
            raise ValidationError(_('Invalid weight - The weight must be between 0 and 400 pounds'))
        return data

    def clean_rear_pax_2(self):
        data = self.cleaned_data['rear_pax_2']
        if data < 0 or data > 400:
            raise ValidationError(_('Invalid weight - The weight must be between 0 and 400 pounds'))
        return data

    def clean_cargo_1(self):
        data = self.cleaned_data['cargo_1']
        if data < 0 or data > 120:
            raise ValidationError(_('Invalid weight - The weight must be between 0 and 120 pounds'))
        return data

    def clean_cargo_2(self):
        data = self.cleaned_data['cargo_2']
        if data < 0 or data > 50:
            raise ValidationError(_('Invalid weight - The weight must be between 0 and 50 pounds'))
        return data

    def clean_fuel_allowance(self):
        data = self.cleaned_data['fuel_allowance']
        if data < 0 or data > 40:
            raise ValidationError(_('Invalid weight - The weight must be between 0 and 40 pounds'))
        return data
