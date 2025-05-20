from ninja import ModelSchema, NinjaAPI

from .models import SensorData
from .signals import sensor_data_received

api = NinjaAPI()

class SensorDataSchema(ModelSchema):
    class Meta:
        model = SensorData
        exclude = ['created_at', "id",]


@api.post("/jardin-data/add", response=SensorDataSchema)
def create_sensor_data(request, payload: SensorDataSchema):
    sensor_data = SensorData.objects.create(**payload.dict())

    # Dispatch the signal with the newly created sensor_data instance
    sensor_data_received.send(
        sender=create_sensor_data,
        sensor_data=sensor_data,
    )

    return sensor_data