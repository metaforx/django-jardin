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