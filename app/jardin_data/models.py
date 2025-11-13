from django.db import models


class SensorData(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()
    device_id = models.CharField(max_length=24)
    sensor_id = models.CharField(max_length=128)
    sensor_name = models.CharField(max_length=255)
    sensor_type = models.CharField(max_length=255)

    class Meta:
        indexes = [
            models.Index(fields=['sensor_id', '-created_at']),
            models.Index(fields=['created_at']),
            models.Index(fields=['value']),
        ]