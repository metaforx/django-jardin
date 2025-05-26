import threading
from typing import Any, Dict, Type
from django.db.models import Model

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import Signal, receiver

from .models import SensorData
from .utils import SignalMessenger

sensor_data_received = Signal()

@receiver(post_save, sender=SensorData)
def send_signal_notification(
    sender: Type[Model],
    instance: 'SensorData',
    created: bool,
    **kwargs: Dict[str, Any]
) -> None:
    """Dispatch a background thread to send a Signal message"""
    if created:
        thread = threading.Thread(
            target=send_notification_background,
            args=(instance.id,)
        )
        thread.daemon = True
        thread.start()



def send_notification_background(instance_id: int) -> bool:
    """Send a Signal message in the background"""
    try:
        instance = SensorData.objects.get(id=instance_id)

        # Initialize the messenger
        messenger = SignalMessenger()

        # Create a nicely formatted message
        message = (
            f"🔔 New Sensor Test Data Alert!\n\n"
            f"Sensor: {instance.sensor_name}\n"
            f"ID: {instance.sensor_id}\n"
            f"Value: {instance.value}\n"
            f"Type: {instance.sensor_type}\n"
            f"Timestamp: {instance.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
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

        # Optionally log success/failure
        if not success:
            print(f"Failed to send Signal message: {output}")

        return success

    except Exception as e:
        # Log any errors that occur
        print(f"Error sending Signal notification: {e}")
        return False
