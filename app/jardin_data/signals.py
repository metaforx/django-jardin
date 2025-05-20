# your_app/signals.py
from django.dispatch import Signal, receiver
from utils import SignalMessenger
from django.conf import settings

sensor_data_received = Signal()

@receiver(sensor_data_received)
def send_signal_notification(sender, sensor_data, **kwargs):
    """Send a Signal message when the sensor_data_received signal is dispatched"""
    messenger = SignalMessenger()

    # Create a nicely formatted message
    message = (
        f"🔔 New Sensor Data Alert!\n\n"
        f"Sensor: {sensor_data.sensor_name}\n"
        f"Value: {sensor_data.value} {sensor_data.unit}\n"
        f"Timestamp: {sensor_data.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    )

    # Send to the single recipient
    recipient = settings.SIGNAL_RECIPIENT
    success, output = messenger.send_message(recipient, message)

    return success
