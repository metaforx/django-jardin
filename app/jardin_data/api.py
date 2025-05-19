from ninja import ModelSchema, NinjaAPI

from .models import SensorData

api = NinjaAPI()

class CreateSensorDataSchema(ModelSchema):
    class Meta:
        model = SensorData
        exclude = ['created_at']


class SensorDataSchema(ModelSchema):
    class Meta:
        model = SensorData
        fields = '__all__'


@api.post("/sensor-data", response=SensorDataSchema)
def create_sensor_data(request, payload: CreateSensorDataSchema):
    sensor_data = SensorData.objects.create(**payload.dict())
    return sensor_data