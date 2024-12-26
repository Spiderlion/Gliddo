from typing import Dict, List, Optional, Any, Tuple
import openai
from datetime import datetime, timezone, timedelta
import json
import logging
from database import SupabaseManager
from pydantic import BaseModel
from enum import Enum

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
    blockers: Optional[List[str]]
    dependencies: Optional[List[str]]

class AIAgent:
    def __init__(self, openai_api_key: str):
        """Initialize the enhanced AI Agent"""
        openai.api_key = openai_api_key
        self.db = SupabaseManager()

    async def detailed_task_analysis(self, response_text: str) -> Dict[str, Any]:
        """Perform detailed analysis of tasks with dependencies and blockers"""
        try:
            prompt = f"""
            Analyze the following employee update in detail:

            {response_text}

            Provide a comprehensive analysis including:
            1. Break down of each task
            2. Dependencies between tasks
            3. Potential blockers
            4. Time estimates
            5. Priority levels
            6. Current status
            7. Completion percentage
            8. Risk factors

            Format the response as JSON with the following structure:
            {{
                "tasks": [
                    {{
                        "name": "task name",
                        "description": "detailed description",
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
                    {"role": "system", "content": "You are an AI project manager analyzing task updates."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )

            return json.loads(completion.choices[0].message.content)
        except Exception as e:
            logging.error(f"Error in detailed_task_analysis: {str(e)}")
            raise

    async def analyze_workload_distribution(self, employee_id: str) -> Dict[str, Any]:
        """Analyze employee workload and task distribution"""
        try:
            # Get recent task history
            history = await self._get_employee_history(employee_id)
            
            prompt = f"""
            Analyze the following employee task history for workload distribution:

            {json.dumps(history)}

            Provide analysis of:
            1. Daily task load
            2. Task complexity distribution
            3. Time allocation across different priorities
            4. Work-life balance indicators
            5. Productivity patterns
            6. Recommendations for workload optimization

            Return as JSON with metrics and recommendations.
            """

            completion = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI workforce analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )

            return json.loads(completion.choices[0].message.content)
        except Exception as e:
            logging.error(f"Error in analyze_workload_distribution: {str(e)}")
            raise

    async def predict_task_completion(self, task_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Predict task completion times and potential delays"""
        try:
            prompt = f"""
            Based on this task analysis:

            {json.dumps(task_analysis)}

            Predict:
            1. Expected completion dates
            2. Probability of delays
            3. Critical path tasks
            4. Risk factors
            5. Mitigation suggestions

            Return as JSON with predictions and confidence levels.
            """

            completion = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI project prediction specialist."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )

            return json.loads(completion.choices[0].message.content)
        except Exception as e:
            logging.error(f"Error in predict_task_completion: {str(e)}")
            raise

    async def analyze_communication_quality(self, response_text: str) -> Dict[str, Any]:
        """Analyze the quality and effectiveness of communication"""
        try:
            prompt = f"""
            Analyze this communication:

            {response_text}

            Evaluate:
            1. Clarity of communication
            2. Completeness of information
            3. Professional tone
            4. Action items clarity
            5. Follow-up requirements
            6. Areas for improvement

            Return as JSON with scores and suggestions.
            """

            completion = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI communication analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )

            return json.loads(completion.choices[0].message.content)
        except Exception as e:
            logging.error(f"Error in analyze_communication_quality: {str(e)}")
            raise

    async def generate_adaptive_feedback(self, 
                                      employee_id: str, 
                                      task_analysis: Dict[str, Any],
                                      communication_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized feedback based on multiple analysis factors"""
        try:
            # Get employee history and preferences
            history = await self._get_employee_history(employee_id)
            
            prompt = f"""
            Based on:
            Task Analysis: {json.dumps(task_analysis)}
            Communication Analysis: {json.dumps(communication_analysis)}
            History: {json.dumps(history)}

            Generate:
            1. Personalized feedback
            2. Specific improvement suggestions
            3. Recognition of strengths
            4. Development areas
            5. Action items
            6. Support needed

            Format as JSON with structured feedback and action items.
            """

            completion = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an AI performance coach."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            feedback = json.loads(completion.choices[0].message.content)
            
            # Store feedback for learning
            await self._store_feedback(employee_id, feedback)
            
            return feedback
        except Exception as e:
            logging.error(f"Error in generate_adaptive_feedback: {str(e)}")
            raise

    async def _store_feedback(self, employee_id: str, feedback: Dict[str, Any]) -> None:
        """Store generated feedback for future reference"""
        try:
            await self.db.create_feedback_record(
                employee_id=employee_id,
                feedback_content=json.dumps(feedback),
                created_at=datetime.now(timezone.utc).isoformat()
            )
        except Exception as e:
            logging.error(f"Error storing feedback: {str(e)}")
            raise

# Example usage
if __name__ == "__main__":
    import asyncio
    from dotenv import load_dotenv
    import os

    async def test_enhanced_analysis():
        load_dotenv()
        agent = AIAgent(os.getenv("OPENAI_API_KEY"))

        # Test detailed task analysis
        response = """
        Today I'm working on:
        1. Website redesign - About 60% complete, waiting for client feedback on color scheme
        2. Client presentation - Started gathering materials, need input from design team
        3. Bug fixes for mobile app - Critical priority, about 30% done
        """

        try:
            analysis = await agent.detailed_task_analysis(response)
            print("\nDetailed Task Analysis:")
            print(json.dumps(analysis, indent=2))

            # Test communication quality
            comm_analysis = await agent.analyze_communication_quality(response)
            print("\nCommunication Quality Analysis:")
            print(json.dumps(comm_analysis, indent=2))
        except Exception as e:
            logging.error(f"Error during testing: {str(e)}")

    asyncio.run(test_enhanced_analysis())