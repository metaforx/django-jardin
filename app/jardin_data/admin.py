from django.contrib import admin
from django.contrib.admin import register

from .models import SensorData


@register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = (
        'device_id',
        'sensor_id',
        'sensor_name',
        'sensor_type',
        'value',
        'created_at',
    )

    model = SensorData