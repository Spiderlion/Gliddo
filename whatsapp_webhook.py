from fastapi import FastAPI, Request
from integrator import WhatsAppIntegrator

app = FastAPI()
wa_integrator = WhatsAppIntegrator()

@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    data = await request.json()
    return await wa_integrator.process_webhook(data)