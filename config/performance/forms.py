from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import CSVFile


class CSVFileForm(forms.ModelForm):
    class Meta:
        model = CSVFile
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data['file']
        if file and not file.name.endswith('.csv'):
            raise forms.ValidationError("File type not supported. Please upload a CSV file")
        return file


class ManualForm(forms.Form):

    error_css_class = "error"

    # Radio choices.
    TANK_VOLUME = [
        ('40', '40 gal'),
        ('50', '50 gal'),
    ]

    RUNWAY_CONDITION = [
        ('PD', 'Paved dry'),
        ('GD', 'Grass dry'),
    ]

    WIND_DIRECTION = [
        ('H', 'Headwind'),
        ('T', 'Tailwind'),
    ]

    # General fields.
    to_weight = forms.IntegerField(min_value=1397, max_value=2300,
                                   widget=forms.TextInput(attrs={'placeholder': 'Takeoff weight in lb'}))
    fuel_capacity = forms.ChoiceField(widget=forms.RadioSelect, choices=TANK_VOLUME)

    # Takeoff fields.
    to_rwy = forms.IntegerField(min_value=1, max_value=360,
                                widget=forms.TextInput(attrs={'placeholder': 'Takeoff runway heading (ex: 070)'}))
    to_length = forms.IntegerField(min_value=0,
                                   widget=forms.TextInput(attrs={'placeholder': 'Takeoff runway length in ft'}))
    to_condition = forms.ChoiceField(widget=forms.RadioSelect, choices=RUNWAY_CONDITION)
    to_press_alt = forms.IntegerField(min_value=0, max_value=14200,
                                      widget=forms.TextInput(attrs={'placeholder': 'Takeoff pressure altitude in ft'}))
    to_temp = forms.IntegerField(min_value=-20, max_value=40,
                                 widget=forms.TextInput(attrs={'placeholder': 'Takeoff temperature in °C'}))
    to_wind_speed = forms.IntegerField(min_value=0, max_value=35,
                                       widget=forms.TextInput(attrs={'placeholder': 'Takeoff wind speed in kts'}))
    to_wind_direction = forms.IntegerField(min_value=1, max_value=360,
                                           widget=forms.TextInput(attrs={'placeholder': 'Takeoff wind direction (ex: 040)'}))

    # Cruise fields.
    travel_dist = forms.IntegerField(min_value=0, max_value=750,
                                     widget=forms.TextInput(attrs={'placeholder': 'Travel distance in nm'}))
    cr_heading = forms.IntegerField(min_value=1, max_value=360,
                                    widget=forms.TextInput(attrs={'placeholder': 'Cruise heading (ex: 090)'}))
    cr_press_alt = forms.IntegerField(min_value=0, max_value=14200,
                                      widget=forms.TextInput(attrs={'placeholder': 'Cruise pressure altitude in ft'}))
    cr_temp = forms.IntegerField(min_value=-20, max_value=40,
                                 widget=forms.TextInput(attrs={'placeholder': 'Cruise temperature in °C'}))
    cr_wind_speed = forms.IntegerField(min_value=0, max_value=50,
                                       widget=forms.TextInput(attrs={'placeholder': 'Cruise wind speed in kts'}))
    cr_wind_direction = forms.IntegerField(min_value=1, max_value=360,
                                           widget=forms.TextInput(attrs={'placeholder': 'Cruise wind direction (ex: 120)'}))
    cr_power = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Cruise rpm'}))
    
    # Landing fields.
    land_rwy = forms.IntegerField(min_value=1, max_value=360,
                                  widget=forms.TextInput(attrs={'placeholder': 'Landing runway heading (ex: 270)'}))
    land_length = forms.IntegerField(min_value=0,
                                     widget=forms.TextInput(attrs={'placeholder': 'Landing runway length in ft'}))
    land_condition = forms.ChoiceField(widget=forms.RadioSelect, choices=RUNWAY_CONDITION)
    land_press_alt = forms.IntegerField(min_value=0, max_value=14200,
                                        widget=forms.TextInput(attrs={'placeholder': 'Landing pressure altitude in ft'}))
    land_temp = forms.IntegerField(min_value=-20, max_value=40,
                                   widget=forms.TextInput(attrs={'placeholder': 'Landing temperature in °C'}))
    land_wind_speed = forms.IntegerField(min_value=0, max_value=35,
                                         widget=forms.TextInput(attrs={'placeholder': 'Landing wind speed in kts'}))
    land_wind_direction = forms.IntegerField(min_value=1, max_value=360,
                                             widget=forms.TextInput(attrs={'placeholder': 'Landing wind direction (ex: 180)'}))
    
    # General data validation.
    def clean_to_weight(self):
        data = self.cleaned_data['to_weight']
        if data < 1397 or data > 2300:
            raise ValidationError(_('Invalid weight - The weight must be between 1397 and 2300 pounds'))
        return data

    # Takeoff data validation.
    def clean_to_rwy(self):
        data = self.cleaned_data['to_rwy']
        if data < 1 or data > 360:
            raise ValidationError(_('Invalid value - The runway heading must be a multiple of 5 between 1 and 360'))
        return data

    def clean_to_length(self):
        data = self.cleaned_data['to_length']
        if data <= 0:
            raise ValidationError(_('Invalid value - The runway length must be bigger than 0'))
        return data

    def clean_to_press_alt(self):
        data = self.cleaned_data['to_press_alt']
        if data < 0 or data > 14200:
            raise ValidationError(_('Invalid value - The altitude must be between 0 and 14200 feets'))
        return data

    def clean_to_temp(self):
        data = self.cleaned_data['to_temp']
        if data < -20 or data > 40:
            raise ValidationError(_('Invalid value - The temperature must be between -20 and 40 degrees Celsius'))
        return data

    def clean_to_wind_speed(self):
        data = self.cleaned_data['to_wind_speed']
        if data < 0 or data > 35:
            raise ValidationError(_('Invalid value - The wind speed must be between 0 and 35 knots'))
        return data

    def clean_to_wind_direction(self):
        data = self.cleaned_data['to_wind_direction']
        if data < 1 or data > 360 or data % 5 != 0:
            raise ValidationError(_('Invalid value - The wind direction must be a multiple of 5 between 1 and 360'))
        return data

    # Cruise data validation.
    def clean_travel_dist(self):
        data = self.cleaned_data['travel_dist']
        if data < 0 or data > 750:
            raise ValidationError(_('Invalid value - The distance must be between 0 and 750 nautical miles'))
        return data

    def clean_cr_heading(self):
        data = self.cleaned_data['cr_heading']
        if data < 1 or data > 360 or data % 5 != 0:
            raise ValidationError(_('Invalid value - The heading must be a multiple of 5 between 1 and 360'))
        return data

    def clean_cr_press_alt(self):
        data = self.cleaned_data['cr_press_alt']
        if data < 0 or data > 14200:
            raise ValidationError(_('Invalid value - The altitude must be between 0 and 14200 feets'))
        return data

    def clean_cr_temp(self):
        data = self.cleaned_data['cr_temp']
        if data < -20 or data > 40:
            raise ValidationError(_('Invalid value - The temperature must be between -20 and 40 degrees Celsius'))
        return data

    def clean_cr_wind_speed(self):
        data = self.cleaned_data['cr_wind_speed']
        if data < 0 or data > 50:
            raise ValidationError(_('Invalid value - The wind speed must be between 0 and 50 knots'))
        return data

    def clean_cr_wind_direction(self):
        data = self.cleaned_data['cr_wind_direction']
        if data < 1 or data > 360 or data % 5 != 0:
            raise ValidationError(_('Invalid value - The wind direction must be a multiple of 5 between 1 and 360'))
        return data

    def clean_cr_power(self):
        data = self.cleaned_data['cr_power']
        if data < 2100 or data > 2650:
            raise ValidationError(_('Invalid value - The rpm must be between 2100 and 2650'))
        return data

    # Landing validation data.
    def clean_land_rwy(self):
        data = self.cleaned_data['land_rwy']
        if data < 1 or data > 360:
            raise ValidationError(_('Invalid value - The runway heading must be a multiple of 5 between 1 and 360'))
        return data

    def clean_land_length(self):
        data = self.cleaned_data['land_length']
        if data <= 0:
            raise ValidationError(_('Invalid value - The runway length must be bigger than 0'))
        return data

    def clean_land_press_alt(self):
        data = self.cleaned_data['land_press_alt']
        if data < 0 or data > 14200:
            raise ValidationError(_('Invalid value - The altitude must be between 0 and 14200 feets'))
        return data

    def clean_land_temp(self):
        data = self.cleaned_data['land_temp']
        if data < -20 or data > 40:
            raise ValidationError(_('Invalid value - The temperature must be between -20 and 40 degrees Celsius'))
        return data

    def clean_land_wind_speed(self):
        data = self.cleaned_data['land_wind_speed']
        if data < 0 or data > 35:
            raise ValidationError(_('Invalid value - The wind speed must be between 0 and 35 knots'))
        return data

    def clean_land_wind_direction(self):
        data = self.cleaned_data['land_wind_direction']
        if data < 1 or data > 360 or data % 5 != 0:
            raise ValidationError(_('Invalid value - The wind direction must be a multiple of 5 between 1 and 360'))
        return data
        