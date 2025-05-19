from django.db import models

class Sensor(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    type = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']


class SensorData(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_at']