import os
from typing import Dict, List, Any
import requests
import json
import logging
from datetime import datetime
from enhanced_data_manager import EnhancedDataManager
from performance_analyzer import PerformanceAnalyzer
from templates import MessageTemplates
from dynamic_templates import DynamicTemplateGenerator

class WhatsAppIntegrator:
    def __init__(self):
        self.templates = MessageTemplates()
        self.dynamic_templates = DynamicTemplateGenerator()
        self.data_manager = EnhancedDataManager()
        self.performance_analyzer = PerformanceAnalyzer()
        self.api_key = os.getenv("WHAPI_API_KEY")
        self.base_url = "https://whapi.cloud/api"
        
    async def send_message(self, phone_number: str, message: str) -> Dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "text",
            "text": {"body": message}
        }
        
        response = requests.post(
            f"{self.base_url}/messages",
            headers=headers,
            json=payload
        )
        
        await self.data_manager.store_message_log(
            phone_number, 
            "outbound",
            message,
            response.json()
        )
        
        return response.json()

    async def process_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            message = webhook_data["messages"][0]
            phone_number = message["from"]
            message_text = message["text"]["body"]
            
            await self.data_manager.store_message_log(
                phone_number,
                "inbound",
                message_text,
                webhook_data
            )
            
            response = await self.performance_analyzer.evaluate_response_quality(
                message_text,
                {"timestamp": message["timestamp"]}
            )
            
            await self.send_message(
                phone_number,
                "Thank you for your update. Your response has been recorded."
            )
            
            return {"status": "success", "message": "Webhook processed"}
            
        except Exception as e:
            logging.error(f"Webhook processing error: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def send_morning_update_request(self, employee_id: str):
        message = await self.dynamic_templates.generate_personalized_message(
            employee_id,
            "daily_updates/morning"
        )
        employee = await self.data_manager.get_employee(employee_id)
        await self.send_message(employee["whatsapp_number"], message)

    async def send_performance_feedback(self, employee_id: str, performance_data: Dict):
        message = await self.dynamic_templates.generate_personalized_message(
            employee_id,
            "feedback/performance",
            context=performance_data
        )
        employee = await self.data_manager.get_employee(employee_id)
        await self.send_message(employee["whatsapp_number"], message)

    async def send_daily_reminder(self, employee_data: Dict[str, Any]) -> None:
        message = (
            "Hi! Please share your daily updates:\n"
            "1. Tasks completed today\n"
            "2. Any blockers or challenges\n"
            "3. Plans for tomorrow"
        )
        await self.send_message(employee_data["whatsapp_number"], message)

    async def send_weekly_report(self, employee_id: str) -> None:
        insights = await self.performance_analyzer.generate_insights(employee_id)
        report_message = (
            "Weekly Performance Summary:\n"
            f"Completion Rate: {insights['performance_trend']['completion_rate_trend']}%\n"
            "Key Recommendations:\n"
        )
        
        for rec in insights['recommendations'][:2]:
            report_message += f"- {rec['suggestion']}\n"
            
        employee = await self.data_manager.get_employee(employee_id)
        await self.send_message(employee["whatsapp_number"], report_message)