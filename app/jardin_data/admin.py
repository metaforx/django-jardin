from django.contrib.admin import register
from unfold.admin import ModelAdmin
from .models import SensorData
import json
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from unfold.views import UnfoldModelAdminViewMixin
from datetime import datetime, timedelta

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
    # Get all unique sensor IDs
    sensor_ids = SensorData.objects.values_list('sensor_id', flat=True).distinct()

    # Prepare color palette for different sensors
    colors = [
        'rgb(239, 68, 68)',    # red
        'rgb(147, 51, 234)',   # purple
        'rgb(234, 179, 8)',    # yellow
        'rgb(34, 197, 94)',    # green
        'rgb(59, 130, 246)',   # blue
        'rgb(236, 72, 153)',   # pink
        'rgb(249, 115, 22)',   # orange
        'rgb(20, 184, 166)',   # teal
    ]

    # Get data for each sensor
    datasets = []
    all_labels = []
    all_values = []

    for idx, sensor_id in enumerate(sensor_ids):
        # Get the latest 10 entries for this sensor
        sensor_data = (
            SensorData.objects
            .filter(sensor_id=sensor_id)
            .order_by('-created_at')[:10]
        )

        # Reverse to show oldest to newest
        sensor_data = list(reversed(sensor_data))

        # Extract values and timestamps
        values = [entry.value for entry in sensor_data]
        labels = [entry.created_at.strftime('%Y-%m-%d %H:%M') for entry in sensor_data]

        # Collect all values for min/max calculation
        all_values.extend(values)

        # Store labels from first sensor (they should all have similar timestamps)
        if idx == 0:
            all_labels = labels

        # Add dataset for this sensor
        color = colors[idx % len(colors)]
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

    # Calculate KPIs
    total_sensors = SensorData.objects.values('sensor_id').distinct().count()
    total_readings_7days = SensorData.objects.filter(
        created_at__gte=datetime.now() - timedelta(days=7)
    ).count()
    total_devices = SensorData.objects.values('device_id').distinct().count()

    # Get recent data for table
    recent_data = SensorData.objects.all()[:10]
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

        "table": {
            "headers": ["Sensor Name", "Sensor ID", "Value", "Timestamp"],
            "rows": table_rows,
        },

        }
    )
    return context