from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_seat_config(seat_config):
    """Raise an exception if the argument is an invalid seat configuration."""
    if seat_config != 0 or seat_config != 1:
        raise ValidationError(_("The seat configuration must 0 (standard) or 1 (optional)"))


def validate_basic_weight(basic_weight):
    """Raise an exception if the argument is an invalid basic empty weight."""
    if basic_weight < 1397 or basic_weight > 2300:
        raise ValidationError(_("Invalid weight - The weight must be between 1397 and 2300 pounds"))


def validate_basic_moment(basic_moment):
    """Raise an exception if the argument is an invalid basic empty moment."""
    if basic_moment < 0 or basic_moment > 120:
        raise ValidationError(_("Invalid moment - The moment must be between 0 and 120 lb-in (/1000)"))


def validate_usable_fuel(usable_fuel):
    """Raise an exception if the argument is an invalid fuel volume."""
    if usable_fuel < 0 or usable_fuel > 50:
        raise ValidationError(_("Invalid volume - The usable fuel must be between 0 and 50 gallons"))


def validate_pilot(pilot):
    """Raise an exception if the argument is an invalid weight."""
    if pilot < 0 or pilot > 400:
        raise ValidationError(_("Invalid weight - The weight must be between 0 and 400 pounds"))


def validate_front_pax(front_pax):
    """Raise an exception if the argument is an invalid weight."""
    if front_pax < 0 or front_pax > 400:
        raise ValidationError(_("Invalid weight - The weight must be between 0 and 400 pounds"))


def validate_rear_pax_left(rear_pax_left):
    """Raise an exception if the argument is an invalid weight."""
    if rear_pax_left < 0 or rear_pax_left > 400:
        raise ValidationError(_("Invalid weight - The weight must be between 0 and 400 pounds"))


def validate_rear_pax_right(rear_pax_right):
    """Raise an exception if the argument is an invalid weight."""
    if rear_pax_right < 0 or rear_pax_right > 400:
        raise ValidationError(_("Invalid weight - The weight must be between 0 and 400 pounds"))


def validate_cargo_1(cargo_1):
    """Raise an exception if the argument is an invalid weight."""
    if cargo_1 < 0 or cargo_1 > 400:
        raise ValidationError(_("Invalid weight - The weight must be between 0 and 400 pounds"))


def validate_cargo_2(cargo_2):
    """Raise an exception if the argument is an invalid weight."""
    if cargo_2 < 0 or cargo_2 > 400:
        raise ValidationError(_("Invalid weight - The weight must be between 0 and 400 pounds"))


def validate_fuel_allowance(fuel_allowance):
    """Raise an exception if the argument is an invalid fuel volume."""
    if fuel_allowance < 0 or fuel_allowance > 2:
        raise ValidationError(_("Invalid volume - The fuel allowance must be between 0 and 2 gallons"))


class CSVFile(models.Model):
    file = models.FileField(upload_to='csvs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class UploadCSVData(models.Model):
    # General fields.
    seat_config = models.PositiveIntegerField(validators=[validate_seat_config])
    basic_weight = models.PositiveIntegerField(validators=[validate_basic_weight])
    basic_moment = models.PositiveIntegerField(validators=[validate_basic_moment])

    # Weight data fields.
    usable_fuel = models.PositiveIntegerField(validators=[validate_usable_fuel])
    pilot = models.PositiveIntegerField(validators=[validate_pilot])
    front_pax = models.PositiveIntegerField(validators=[validate_front_pax])
    rear_pax_1 = models.PositiveIntegerField(validators=[validate_rear_pax_left])
    rear_pax_2 = models.PositiveIntegerField(validators=[validate_rear_pax_right])
    cargo_1 = models.PositiveIntegerField(validators=[validate_cargo_1])
    cargo_2 = models.PositiveIntegerField(validators=[validate_cargo_2])
    fuel_allowance = models.PositiveIntegerField(validators=[validate_fuel_allowance])
