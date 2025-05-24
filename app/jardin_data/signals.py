from django.conf import settings
from django.dispatch import Signal, receiver
from .utils import SignalMessenger

sensor_data_received = Signal()

@receiver(sensor_data_received)
def send_signal_notification(sender, sensor_data, **kwargs):
    """Send a Signal message when the sensor_data_received signal is dispatched"""
    messenger = SignalMessenger()

    # Create a nicely formatted message
    message = (
        f"🔔 New Sensor Test Data Alert!\n\n"
        f"Sensor: {sensor_data.sensor_name}\n"
        f"ID: {sensor_data.sensor_id}\n"
        f"Value: {sensor_data.value}\n"
        f"Type: {sensor_data.sensor_type}\n"
        f"Timestamp: {sensor_data.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        f"Sorry for the disturbance! Have a great day!"
    )

    # Get recipient from settings
    recipient = settings.SIGNAL_RECEIVER_GROUP

    # Send a message to the assigned Signal phone number
    if recipient.startswith("+"):
        success, output = messenger.send_message(recipient, message)
    else:
        # For simplicity, we expect it to be a group id
        success, output = messenger.send_group_message(recipient, message)

    return success
