from django.db import models



class SensorData(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()
    sensor_name = models.CharField(max_length=255)
    sensor_type = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['created_at']