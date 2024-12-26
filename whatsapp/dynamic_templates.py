# dynamic_templates.py

import json
from typing import Dict, Any, Optional
import openai
import logging
from datetime import datetime
from .templates import MessageTemplates
from performance_analyzer import PerformanceAnalyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DynamicTemplateGenerator:
    """
    Generates personalized message templates using AI, based on employee performance
    and context. Combines pre-written templates with dynamic content.
    """
    
    def __init__(self):
        self.base_templates = MessageTemplates()
        self.performance_analyzer = PerformanceAnalyzer()
        
    async def generate_personalized_message(
        self,
        employee_id: str,
        message_type: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate a personalized message based on employee data and context.
        
        Args:
            employee_id: The employee's unique identifier
            message_type: Type of message to generate
            context: Additional context for message generation
            
        Returns:
            Personalized message string
        """
        try:
            # Get employee performance insights
            insights = await self.performance_analyzer.generate_insights(employee_id)
            
            # Create AI prompt based on message type and context
            prompt = self._create_prompt(message_type, insights, context)
            
            # Generate personalized content using GPT-3.5
            response = await openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating personalized message: {str(e)}")
            # Fallback to base template
            return self.base_templates.get_template(
                message_type.split('/')[0],
                message_type.split('/')[1]
            )
    
    def _create_prompt(
        self,
        message_type: str,
        insights: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create an AI prompt based on message type and context.
        """
        base_prompts = {
            "daily_updates/morning": f"""
Create a personalized morning update request message considering:
- Previous completion rate: {insights['performance_trend']['completion_rate_trend']}%
- Recent task patterns: {insights['common_tasks']}
- Current recommendations: {insights['recommendations']}

The message should be:
1. Professional but friendly
2. Include specific references to their work patterns
3. Use appropriate emojis for WhatsApp
4. Be motivating and encouraging
            """.strip(),
            
            "feedback/performance": f"""
Generate constructive feedback based on:
- Quality trends: {insights['performance_trend']['quality_trend']}
- Task completion patterns: {insights['common_tasks']}
- Areas for improvement: {insights['recommendations']}

The feedback should be:
1. Specific and actionable
2. Balanced between praise and improvement areas
3. Encouraging and supportive
4. Include concrete next steps
            """.strip()
        }
        
        # Add any additional context to the prompt
        if context:
            base_prompts[message_type] += f"\n\nAdditional context:\n{json.dumps(context, indent=2)}"
            
        return base_prompts.get(
            message_type,
            "Generate a professional and friendly message appropriate for WhatsApp."
        )