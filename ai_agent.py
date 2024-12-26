from typing import Dict, List, Optional, Any
import openai
from datetime import datetime, timezone
import json
import logging
from database import SupabaseManager
from pydantic import BaseModel
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Enhanced data models
class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class TaskStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    DELAYED = "delayed"

class TaskAnalysis(BaseModel):
    task_name: str
    description: str
    priority: Priority
    status: TaskStatus
    estimated_hours: float
    completion_percentage: float
    blockers: Optional[List[str]] = []
    dependencies: Optional[List[str]] = []

class AIAgent:
    def __init__(self, openai_api_key: str):
        """Initialize the enhanced AI Agent"""
        if not openai_api_key:
            raise ValueError("OpenAI API key is required.")
        
        openai.api_key = openai_api_key
        self.db = SupabaseManager()

    def process_message(self, message: str) -> str:
        """
        Process the incoming message and generate a response using OpenAI.
        """
        try:
            prompt = f"You are a helpful assistant. Respond to the following message: {message}"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            logger.error(f"Error in process_message: {str(e)}")
            return "Sorry, I encountered an error processing your message."

    async def detailed_task_analysis(self, response_text: str) -> Dict[str, Any]:
        """
        Perform detailed analysis of tasks with dependencies and blockers.
        """
        try:
            prompt = f"""
            Analyze the following employee update in detail:

            {response_text}

            Provide a comprehensive analysis including:
            1. Task breakdown
            2. Dependencies
            3. Blockers
            4. Estimated hours
            5. Priority levels
            6. Current status
            7. Completion percentage
            8. Risks

            Format the response as JSON with the following structure:
            {{
                "tasks": [
                    {{
                        "name": "task name",
                        "description": "description",
                        "priority": "high/medium/low",
                        "status": "not_started/in_progress/completed/blocked/delayed",
                        "estimated_hours": float,
                        "completion_percentage": float,
                        "blockers": ["blocker1", "blocker2"],
                        "dependencies": ["dependency1", "dependency2"],
                        "risks": ["risk1", "risk2"]
                    }}
                ],
                "overall_assessment": "assessment text",
                "recommendations": ["rec1", "rec2"]
            }}
            """

            completion = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI task analysis expert."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3
            )

            # Log the full response for debugging
            logger.info(f"OpenAI Response: {completion}")

            # Extract the content and clean up the JSON string
            response_content = completion["choices"][0]["message"]["content"]
            clean_json = response_content.strip("```json").strip("```")

            # Parse and return the cleaned JSON content
            return json.loads(clean_json)
        except json.JSONDecodeError as e:
            logger.error(f"Error in detailed_task_analysis: {str(e)} - Full Response: {completion}")
            return {"error": f"Invalid JSON response: {str(e)}"}
        except Exception as e:
            logger.error(f"Error in detailed_task_analysis: {str(e)}")
            return {"error": str(e)}

# Example usage
if __name__ == "__main__":
    import asyncio
    from dotenv import load_dotenv
    import os

    async def test_ai_agent():
        load_dotenv()
        openai_api_key = os.getenv("OPENAI_API_KEY")
        agent = AIAgent(openai_api_key)

        response = "Today I worked on redesigning the website and fixing bugs in the mobile app."

        try:
            analysis = await agent.detailed_task_analysis(response)
            print("Detailed Task Analysis:", json.dumps(analysis, indent=2))
        except Exception as e:
            logger.error(f"Error in test_ai_agent: {str(e)}")

    asyncio.run(test_ai_agent())
