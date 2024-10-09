from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_to_weight(to_weight):
    """Raise an exception if the argument is an invalid aircraft weight."""
    if to_weight < 1397 or to_weight > 2300:
        raise ValidationError(_("The weight must be between 1397 and 2300 pounds"))


def validate_fuel_capacity(fuel_capacity):
    """Raise an exception if the argument is an invalid fuel capacity."""
    if fuel_capacity != 40 and fuel_capacity != 50:
        raise ValidationError(_("The fuel capacity must be 40 or 50"))


def validate_heading(heading):
    """Raise an exception if the argument is an invalid heading."""
    if heading < 1 or heading > 360:
        raise ValidationError(_("{} is not a valid heading".format(heading)))


def validate_runway_length(rwy_length):
    """Raise an exception if the argument is an invalid runway length."""
    if rwy_length <= 0:
        raise ValidationError(_("The runway length must be bigger than zero"))


def validate_runway_condition(rwy_condition):
    """Raise an exception if the argument is an invalid runway condition."""
    valid_conditions = ['p', 'g']
    if rwy_condition.lower() not in valid_conditions:
        raise ValidationError(_("{} is not a valid runway condition".format(rwy_condition)))


def validate_pressure_altitude(press_altitude):
    """Raise an exception if the argument is an invalid pressure altitude."""
    if press_altitude < 0 or press_altitude > 14200:
        raise ValidationError(_("The pressure altitude must be between 0 and 14200 fts"))


def validate_temperature(temp):
    """Raise an exception if the argument is an invalid temperature."""
    if temp < -20 or temp > 40:
        raise ValidationError(_("The temperature must be between -20 and 40 degrees Celsius"))


def validate_wind_speed(wind_speed):
    """Raise an exception if the argument is an invalid wind speed."""
    if wind_speed < 0 or wind_speed > 50:
        raise ValidationError(_("The wind speed must be between 0 and 50 kts"))


def validate_wind_direction(wind_direction):
    """Raise an exception if the argument is an invalid wind direction."""
    if wind_direction < 1 or wind_direction > 360 or wind_direction % 5 != 0:
        raise ValidationError(_("{} is not a valid wind direction".format(wind_direction)))


def validate_travel_distance(travel_distance):
    """Raise an exception if the argument is an invalid travel distance."""
    if travel_distance < 0 or travel_distance > 750:
        raise ValidationError(_("The travel distance must be between 0 and 750 nm"))


def validate_cruise_rpm(cr_rpm):
    """Raise an exception if the argument is an invalid cruise rpm."""
    if cr_rpm < 2100 or cr_rpm > 2650:
        raise ValidationError(_("{} is not a valid cruise rpm".format(cr_rpm)))
