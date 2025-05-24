from django.db import models



class SensorData(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()
    sensor_id = models.CharField(max_length=24)
    sensor_name = models.CharField(max_length=255)
    sensor_type = models.CharField(max_length=255)

    class Meta:
        ordering = ['-created_at']