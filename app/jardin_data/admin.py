from django.contrib import admin
from django.contrib.admin import register

from .models import Sensor, SensorData


@register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'type',
    )

    model = Sensor


@register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'value',
        'sensor',
        'created_at',
    )

    list_filter = ('sensor',)

    model = SensorData