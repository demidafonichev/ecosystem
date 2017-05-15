from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Box(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(
        max_length=30,
        unique=False,
        null=True,
        blank=True,
        default='unregistered',
        help_text=_('Name for box to differ boxes with same plant')
    )

    key = models.CharField(
        max_length=10,
        help_text=_('Security key')
    )

    plant = models.ForeignKey(
        'box.Plant',
        blank=True,
        null=True,
        help_text=_('Plant name')
    )

    registered = models.BooleanField(
        default=False,
        help_text=_('Displays if the box is registered')
    )

    owner = models.ForeignKey(
        User,
        blank=True,
        null=True,
        help_text=_('User-owner of box')
    )

    care = models.ForeignKey(
        'box.CareMethod',
        blank=True,
        null=True,
        help_text=_('Plant custom care method')
    )

    temperature = models.FloatField(
        default=-1.,
        null=True,
        help_text=_('Temperature inside box')
    )

    air_humidity = models.FloatField(
        default=-1.,
        null=True,
        help_text=_('Air humidity inside box')
    )

    soil_humidity = models.FloatField(
        default=-1.,
        null=True,
        help_text=_('Soil humidity inside box')
    )

    status = models.BooleanField(
        default=False,
        help_text=_('Box connection status')
    )


class Plant(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(
        max_length=30,
        null=True,
        unique=True,
        blank=False,
        help_text=_('Plant name')
    )

    care = models.ForeignKey(
        'box.CareMethod',
        null=True,
        help_text=_('Plant default care method')
    )


class CareMethod(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(
        max_length=20,
        null=True,
        default='unnamed',
        help_text=_('Name for care method to differ them on admin')
    )

    is_watering_default = models.BooleanField(
        default=True,
        help_text=_('Flag is watering default or custom')
    )

    is_illumination_default = models.BooleanField(
        default=True,
        help_text=_('Flag is illumination default or custom')
    )


class Watering(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(
        max_length=30,
        default='unnamed',
        help_text=_('Name for watering object to differ them on admin')
    )

    watering_start_time = models.IntegerField(
        help_text=_('Time to start watering plant')
    )

    watering_volume = models.IntegerField(
        help_text=_('Volume of water to watering plant')
    )

    watering_frequency = models.CharField(
        max_length=16,
        help_text=_('Care frequency')
    )

    care_method = models.ForeignKey(
        'box.CareMethod',
        null=True,
        help_text=_('Pointer to care method watering belongs to')
    )


class Illumination(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(
        max_length=30,
        default='unnamed',
        help_text=_('Name for illumination object to differ them on admin')
    )

    illumination_start_time = models.IntegerField(
        help_text=_('Time to start illumination'),
    )

    illumination_duration_time = models.IntegerField(
        help_text=_('Time to end illumination')
    )

    illumination_frequency = models.CharField(
        max_length=16,
        help_text=_('Care frequency')
    )

    care_method = models.ForeignKey(
        'box.CareMethod',
        null=True,
        help_text=_('Pointer to care method watering belongs to')
    )
