from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class PerformanceData(forms.Form):

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
    to_weight = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Takeoff weight in lb'}))
    fuel_capacity = forms.ChoiceField(widget=forms.RadioSelect, choices=TANK_VOLUME)

    # Takeoff fields.
    to_length = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Takeoff runway length in ft'}))
    to_condition = forms.ChoiceField(widget=forms.RadioSelect, choices=RUNWAY_CONDITION)
    to_press_alt = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Takeoff pressure altitude in ft'}))
    to_temp = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Takeoff temperature in °C'}))
    to_wind_speed = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Takeoff wind speed in kts'}))
    to_wind_direction = forms.ChoiceField(widget=forms.RadioSelect, choices=WIND_DIRECTION)

    # Cruise fields.
    travel_dist = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Travel distance in nm'}))
    cr_press_alt = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Cruise pressure altitude in ft'}))
    cr_temp = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Cruise temperature in °C'}))
    cr_wind_speed = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Cruise wind speed in kts'}))
    cr_wind_direction = forms.ChoiceField(widget=forms.RadioSelect, choices=WIND_DIRECTION)
    cr_power = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Cruise rpm'}))
    
    # Landing fields.
    land_length = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Landing runway length in ft'}))
    land_condition = forms.ChoiceField(widget=forms.RadioSelect, choices=RUNWAY_CONDITION)
    land_press_alt = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Landing pressure altitude in ft'}))
    land_temp = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Landing temperature in °C'}))
    land_wind_speed = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Landing wind speed in kts'}))
    land_wind_direction = forms.ChoiceField(widget=forms.RadioSelect, choices=WIND_DIRECTION)
    
    # General data validation.
    def clean_to_weight(self):
        data = self.cleaned_data['to_weight']
        if data < 1397 or data > 2300:
            raise ValidationError(_('Invalid weight - The weight must be between 1397 and 2300 pounds'))
        return data


    # Takeoff data validation.
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
        if data < 0:
            raise ValidationError(_('Invalid value - The wind speed must be a positive value'))
        return data


    # Cruise data validation.
    def clean_travel_dist(self):
        data = self.cleaned_data['travel_dist']
        if data < 0:
            raise ValidationError(_('Invalid value - The distance must be a positive value'))
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
        if data < 0:
            raise ValidationError(_('Invalid value - The wind speed must be a positive value'))
        return data


    def clean_cr_power(self):
        data = self.cleaned_data['cr_power']
        if data < 2100 or data > 2650:
            raise ValidationError(_('Invalid value - The rpm must be between 2100 and 2650'))
        return data


    # Landing validation data.
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
        if data < 0:
            raise ValidationError(_('Invalid value - The wind speed must be a positive value'))
        return data
        