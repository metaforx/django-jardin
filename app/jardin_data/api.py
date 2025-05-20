from ninja import ModelSchema, NinjaAPI

from .models import SensorData

api = NinjaAPI()

class SensorDataSchema(ModelSchema):
    class Meta:
        model = SensorData
        exclude = ['created_at']


@api.post("/sensor-data", response=SensorDataSchema)
def create_sensor_data(request, payload: SensorDataSchema):
    sensor_data = SensorData.objects.create(**payload.dict())
    return sensor_data