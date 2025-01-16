import os
import aiohttp
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class WhatsAppService:
    def __init__(self):
        """Initialize the WhatsAppService with the Whapi API key and base URL."""
        self.api_key = os.getenv("WHAPI_API_KEY")  # Use your API key
        self.base_url = "https://glito.whapi.com"  # Use the API URL from the dashboard
        
    async def send_text_message(self, phone_number: str, message: str) -> Dict[str, Any]:
        """
        Send a text message via WhatsApp.

        :param phone_number: The recipient's phone number in international format.
        :param message: The text message to send.
        :return: Response from the API.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "typing_time": 0,  # Optional typing simulation
            "to": phone_number,
            "body": message
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.base_url}/messages/text",
                    headers=headers,
                    json=payload
                ) as response:
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientError as e:
                logger.error(f"Error sending WhatsApp message: {str(e)}")
                raise

    async def send_template_message(self, phone_number: str, template_name: str, 
                                  components: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Send a template message.

        :param phone_number: The recipient's phone number in international format.
        :param template_name: The name of the template to send.
        :param components: Optional components for the template.
        :return: Response from the API.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "to": phone_number,
            "template": {
                "name": template_name,
                "language": {
                    "code": "en"
                }
            }
        }
        
        if components:
            payload["template"]["components"] = components

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.base_url}/messages/template",
                    headers=headers,
                    json=payload
                ) as response:
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientError as e:
                logger.error(f"Error sending template message: {str(e)}")
                raise

    async def send_media_message(self, phone_number: str, media_type: str, 
                               media_url: str, caption: Optional[str] = None) -> Dict[str, Any]:
        """
        Send a media message (image, video, document).

        :param phone_number: The recipient's phone number in international format.
        :param media_type: The type of media (e.g., image, video, document).
        :param media_url: The URL of the media file.
        :param caption: Optional caption for the media.
        :return: Response from the API.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "to": phone_number,
            "type": media_type,
            "media": {
                "url": media_url
            }
        }
        
        if caption:
            payload["media"]["caption"] = caption

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.base_url}/messages/media",
                    headers=headers,
                    json=payload
                ) as response:
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientError as e:
                logger.error(f"Error sending media message: {str(e)}")
                raise

    async def mark_message_as_read(self, message_id: str) -> Dict[str, Any]:
        """
        Mark a message as read.

        :param message_id: The ID of the message to mark as read.
        :return: Response from the API.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    f"{self.base_url}/messages/{message_id}/read",
                    headers=headers
                ) as response:
                    response.raise_for_status()
                    return await response.json()
            except aiohttp.ClientError as e:
                logger.error(f"Error marking message as read: {str(e)}")
                raise