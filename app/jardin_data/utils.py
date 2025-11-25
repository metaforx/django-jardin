from typing import Tuple, Literal

import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

class SignalMessenger:
    """Signal messenger class that calls the Signal REST API"""

    def __init__(self):
        self.phone_number = settings.SIGNAL_PHONE_NUMBER
        self.api_base_url = settings.SIGNAL_API_BASE_URL

    def send_message(
        self,
        recipient: str,
        message: str,
        text_mode: Literal["normal", "urgent", "preview"] = "normal",
    ) -> Tuple[bool, str]:
        """
        Send a Signal message to a recipient using the REST API

        Args:
            recipient (str): Phone number of the recipient in international format (e.g. +1234567890)
            message (str): The message text to send
            text_mode (str, optional): Text mode, either "normal" or "styled"

        Returns:
            tuple: (success, response_or_error)
        """
        try:
            url = f"{self.api_base_url}/v2/send"

            # Build the payload according to the schema
            payload = {
                "message": message,
                "number": self.phone_number,
                "recipients": [recipient],
                "text_mode": text_mode,
                "notify_self": True
            }

            response = requests.post(url, json=payload)
            response.raise_for_status()

            logger.info(f"Sent Signal message to {recipient}: {message[:50]}...")
            return True, response.text

        except requests.RequestException as e:
            logger.error(f"Failed to send Signal message: {str(e)}")
            return False, str(e)

    def send_group_message(self, group_id, message, text_mode="normal"):
        """
        Send a Signal message to a group using the REST API

        Args:
            group_id (str): The group ID (base64 encoded)
            message (str): The message text to send
            text_mode (str, optional): Text mode, either "normal" or "styled"

        Returns:
            tuple: (success, response_or_error)
        """
        try:
            url = f"{self.api_base_url}/v2/send"

            clean_group_id = group_id.strip()

            # Correctly format the recipient for group messages
            # The group ID must be prefixed with "group."

            payload = {
                "message": message,
                "number": self.phone_number,  # Sender's registered phone number
                "recipients": [clean_group_id],  # Group ID prefixed with "group."
                "text_mode": text_mode,
                "notify_self": True,  # Optional: To see the message in your own Signal app
            }

            logger.debug(f"Sending group message with payload: {payload} to URL: {url}")

            response = requests.post(url, json=payload)
            response.raise_for_status()  # This will raise an HTTPError for 4xx/5xx responses

            logger.info(f"Sent Signal message to group {group_id}: {message[:50]}...")
            return True, response.text

        except requests.RequestException as e:
            logger.error(f"Failed to send Signal message: {str(e)}")
            return False, str(e)
