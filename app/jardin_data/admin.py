from django.contrib.admin import register
from unfold.admin import ModelAdmin
from .models import SensorData
import json
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from unfold.views import UnfoldModelAdminViewMixin
from datetime import timedelta
from django.utils import timezone

@register(SensorData)
class SensorDataAdmin(ModelAdmin):
    list_display = (
        'device_id',
        'sensor_id',
        'sensor_name',
        'sensor_type',
        'value',
        'created_at',
    )

    model = SensorData


admin.site.index_title = 'Dashboard'


class DashboardView(UnfoldModelAdminViewMixin, TemplateView):
    title = "Dashboard"
    permission_required = ()
    template_name = "admin/index.html"


class DashboardAdmin(ModelAdmin):
    def get_urls(self):
        return super().get_urls() + [
            path(
                "index",
                DashboardView.as_view(model_admin=self),
                name="index"
            ),
        ]


def dashboard_callback(request, context):
    """
    Callback to prepare custom variables for the index template which is used as a dashboard
    template. It can be overridden in the application by creating custom admin/index.html.
    """
    # Color mapping based on sensor ID suffix
    color_mapping = {
        'red': 'rgb(239, 68, 68)',
        'purple': 'rgb(147, 51, 234)',
        'yellow': 'rgb(234, 179, 8)',
        'green': 'rgb(34, 197, 94)',
        'blue': 'rgb(59, 130, 246)',
        'pink': 'rgb(236, 72, 153)',
        'orange': 'rgb(249, 115, 22)',
        'teal': 'rgb(20, 184, 166)',
    }

    # Get all unique sensor IDs in a single query
    sensor_ids = list(SensorData.objects.values_list('sensor_id', flat=True).distinct())
    
    # Map sensor IDs to colors by extracting color from sensor ID
    sensor_color_map = {}
    for sensor_id in sensor_ids:
        # Extract color from sensor ID (e.g., "27003b000547343232363230-0-yellow" -> "yellow")
        color_name = None
        for color_key in color_mapping.keys():
            if sensor_id.endswith(f'-{color_key}'):
                color_name = color_key
                break
        
        # Use the extracted color or default to red
        sensor_color_map[sensor_id] = color_mapping.get(color_name, color_mapping['red'])

    # Fetch all recent sensor data in one query instead of looping
    from django.db.models import Max
    
    # Get the latest 10 entries for each sensor in a single optimized query
    all_sensor_data = (
        SensorData.objects
        .filter(sensor_id__in=sensor_ids)
        .order_by('sensor_id', '-created_at')
    )
    
    # Group data by sensor_id
    sensor_data_grouped = {}
    for data in all_sensor_data:
        if data.sensor_id not in sensor_data_grouped:
            sensor_data_grouped[data.sensor_id] = []
        if len(sensor_data_grouped[data.sensor_id]) < 10:
            sensor_data_grouped[data.sensor_id].append(data)

    # Get data for each sensor
    datasets = []
    all_labels = []
    all_values = []

    for idx, sensor_id in enumerate(sensor_ids):
        # Get the data for this sensor
        sensor_data = sensor_data_grouped.get(sensor_id, [])
        
        # Reverse to show oldest to newest
        sensor_data = list(reversed(sensor_data))

        if not sensor_data:
            continue

        # Extract values and timestamps
        values = [entry.value for entry in sensor_data]
        labels = [entry.created_at.strftime('%Y-%m-%d %H:%M') for entry in sensor_data]

        # Collect all values for min/max calculation
        all_values.extend(values)

        # Store labels from first sensor (they should all have similar timestamps)
        if idx == 0:
            all_labels = labels

        # Add dataset for this sensor
        color = sensor_color_map[sensor_id]
        datasets.append({
            'label': sensor_id,
            'data': values,
            'borderColor': color,
            'backgroundColor': color.replace('rgb', 'rgba').replace(')', ', 0.1)'),
            'tension': 0.4
        })

    # Calculate min and max temperatures for y-axis (round to nearest integer)
    import math
    if all_values:
        min_temp = math.floor(min(all_values))
        max_temp = math.ceil(max(all_values))
    else:
        min_temp = 0
        max_temp = 30

    # Get lowest and highest temperatures from past 7 days in a single query each
    seven_days_ago = timezone.now() - timedelta(days=7)
    
    lowest_temp_reading = (
        SensorData.objects
        .filter(created_at__gte=seven_days_ago)
        .order_by('value')
        .first()
    )
    
    highest_temp_reading = (
        SensorData.objects
        .filter(created_at__gte=seven_days_ago)
        .order_by('-value')
        .first()
    )
    
    # Prepare lowest and highest temp data
    lowest_temp_data = None
    highest_temp_data = None
    
    if lowest_temp_reading:
        lowest_temp_data = {
            'value': lowest_temp_reading.value,
            'sensor_id': lowest_temp_reading.sensor_id,
            'sensor_name': lowest_temp_reading.sensor_name,
            'date': lowest_temp_reading.created_at.strftime('%Y-%m-%d'),
            'time': lowest_temp_reading.created_at.strftime('%H:%M'),
            'color': sensor_color_map.get(lowest_temp_reading.sensor_id, color_mapping['red'])
        }
    
    if highest_temp_reading:
        highest_temp_data = {
            'value': highest_temp_reading.value,
            'sensor_id': highest_temp_reading.sensor_id,
            'sensor_name': highest_temp_reading.sensor_name,
            'date': highest_temp_reading.created_at.strftime('%Y-%m-%d'),
            'time': highest_temp_reading.created_at.strftime('%H:%M'),
            'color': sensor_color_map.get(highest_temp_reading.sensor_id, color_mapping['red'])
        }

    # Calculate KPIs with optimized queries
    total_sensors = len(sensor_ids)
    total_readings_7days = SensorData.objects.filter(
        created_at__gte=seven_days_ago
    ).count()
    total_devices = SensorData.objects.values('device_id').distinct().count()

    # Get recent data for table
    recent_data = SensorData.objects.all().order_by('-created_at')[:10]
    table_rows = []
    for data in recent_data:
        table_rows.append([
            data.sensor_name,
            data.sensor_id,
            f"{data.value}°C" if data.sensor_type == "temperature" else str(data.value),
            data.created_at.strftime('%Y-%m-%d %H:%M'),
        ])

    # Send data to the dashboard
    context.update(
        {
        "kpis": [
            {
                "title": "Total Active Sensors",
                "metric": total_sensors,
            },
            {
                "title": "Readings (Last 7 days)",
                "metric": total_readings_7days,
            },
            {
                "title": "Total Devices",
                "metric": total_devices,
            },
        ],

        "dauChartData": json.dumps({
            'datasets': datasets,
            'labels': all_labels
        }),

        "chartOptions": json.dumps({
            'scales': {
                'y': {
                    'min': min_temp,
                    'max': max_temp,
                    'ticks': {
                        'stepSize': 1
                    },
                    'title': {
                        'display': True,
                        'text': 'Temperature (°C)'
                    }
                }
            },
            'plugins': {
                'legend': {
                    'display': True
                }
            }
        }),

        "dpsChartData": json.dumps({
            'datasets': datasets,
            'labels': all_labels
        }),

        "lowest_temp": lowest_temp_data,
        "highest_temp": highest_temp_data,

        "table": {
            "headers": ["Sensor Name", "Sensor ID", "Value", "Timestamp"],
            "rows": table_rows,
        },

        }
    )
    return context