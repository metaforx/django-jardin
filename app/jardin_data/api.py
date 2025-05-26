from django.http import HttpRequest
from ninja import ModelSchema, NinjaAPI
from ninja_apikey.security import APIKeyAuth

from .models import SensorData
from .signals import sensor_data_received

api = NinjaAPI(auth=APIKeyAuth())

class SensorDataSchema(ModelSchema):
    class Meta:
        model = SensorData
        exclude = ['created_at', "id",]

@api.post("/jardin-data/add", response=SensorDataSchema)
def create_sensor_data(request: HttpRequest, payload: SensorDataSchema) -> SensorData:
    sensor_data = SensorData.objects.create(**payload.dict())
    return sensor_data
