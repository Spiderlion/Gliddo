import os
from fastapi import FastAPI, Request, HTTPException
from typing import Dict, Any
import logging
import asyncio
from whatsapp_service import WhatsAppService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Function to send initial message
async def send_initial_message():
    whatsapp = WhatsAppService()
    try:
        response = await whatsapp.send_text_message(
            phone_number="+91 6299269697",  # Your number
            message="Hello! This is your WhatsApp agent. How can I assist you today?"  # Initial message
        )
        logger.info(f"Initial message sent successfully: {response}")
    except Exception as e:
        logger.error(f"Failed to send initial message: {str(e)}")

# Send initial message when the server starts
@app.on_event("startup")
async def startup_event():
    await send_initial_message()

# Root endpoint
@app.get("/")
async def root():
    return {"message": "WhatsApp Webhook Server is running"}

# Webhook endpoint
@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    try:
        webhook_data = await request.json()
        logger.info(f"Received webhook data: {webhook_data}")  # Log the payload

        # Verify if it's a message notification
        if "messages" in webhook_data:
            message = webhook_data["messages"][0]
            phone_number = message["from"]  # Sender's phone number
            message_text = message["text"]["body"]  # Message content
            message_id = message["id"]  # Unique message ID

            # Log the message details
            logger.info(f"Received message from {phone_number}: {message_text}")

            # Send a response
            response_text = "Thanks for your message! How can I help you today?"
            return {"status": "success", "message": response_text}

        return {"status": "success", "message": "Webhook received"}

    except Exception as e:
        logger.error(f"Error in webhook handler: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)