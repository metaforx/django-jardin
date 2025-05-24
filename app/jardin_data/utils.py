# utils/signal_messenger.py
import logging
import subprocess
from django.conf import settings

logger = logging.getLogger(__name__)

class SignalMessenger:
    """Signal messenger class that calls the signal-cli binary directly"""

    def __init__(self):
        self.phone_number = settings.SIGNAL_PHONE_NUMBER

    def send_message(self, recipient, message):
        """Send a Signal message to a recipient"""
        try:
            cmd = [
                "signal-cli",
                "-u", self.phone_number,
                "send",
                "-m", message,
                recipient
            ]

            result = subprocess.run(
                cmd,
                check=True,
                text=True,
                capture_output=True
            )

            logger.info(f"Sent Signal message to {recipient}: {message[:50]}...")
            return True, result.stdout

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to send Signal message: {e.stderr}")
            return False, e.stderr


    def send_group_message(self, group_id, message):
        """Send a Signal message to a group"""
        try:
            cmd = [
                "signal-cli",
                "-u", self.phone_number,
                "send",
                "-g", group_id,
                "-m", message
            ]

            result = subprocess.run(
                cmd,
                check=True,
                text=True,
                capture_output=True
            )

            logger.info(f"Sent Signal message to group {group_id}: {message[:50]}...")
            return True, result.stdout

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to send Signal group message: {e.stderr}")
            return False, e.stderr
