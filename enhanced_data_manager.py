from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import logging
from supabase import Client, create_client
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedDataManager:
    def __init__(self):
        load_dotenv()
        self.client: Client = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY")
        )

    async def store_task_analysis(self, 
                                employee_id: str, 
                                analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Store AI agent's task analysis results"""
        try:
            data = {
                "employee_id": employee_id,
                "analysis_data": analysis_data,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            result = self.client.table("task_analysis").insert(data).execute()
            return result.data[0]
        except Exception as e:
            logger.error(f"Error storing task analysis: {str(e)}")
            raise

    async def update_employee_metrics(self, 
                                    employee_id: str, 
                                    metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Update employee performance metrics"""
        try:
            result = self.client.table("employees")\
                .update(metrics)\
                .eq("id", employee_id)\
                .execute()
            return result.data[0]
        except Exception as e:
            logger.error(f"Error updating employee metrics: {str(e)}")
            raise

    async def get_employee_performance_history(self, 
                                             employee_id: str,
                                             start_date: str,
                                             end_date: str) -> List[Dict[str, Any]]:
        """Retrieve employee's historical performance data"""
        try:
            result = self.client.table("daily_tasks")\
                .select("*")\
                .eq("employee_id", employee_id)\
                .gte("task_date", start_date)\
                .lte("task_date", end_date)\
                .execute()
            return result.data
        except Exception as e:
            logger.error(f"Error retrieving performance history: {str(e)}")
            raise

    async def store_ai_feedback(self,
                              employee_id: str,
                              feedback_type: str,
                              feedback_content: Dict[str, Any]) -> Dict[str, Any]:
        """Store AI-generated feedback"""
        try:
            data = {
                "employee_id": employee_id,
                "feedback_type": feedback_type,
                "feedback_content": feedback_content,
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            result = self.client.table("ai_feedback").insert(data).execute()
            return result.data[0]
        except Exception as e:
            logger.error(f"Error storing AI feedback: {str(e)}")
            raise

    async def get_recent_interactions(self,
                                    employee_id: str,
                                    limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve recent AI-employee interactions"""
        try:
            result = self.client.table("message_logs")\
                .select("*")\
                .eq("employee_id", employee_id)\
                .order("sent_at", desc=True)\
                .limit(limit)\
                .execute()
            return result.data
        except Exception as e:
            logger.error(f"Error retrieving recent interactions: {str(e)}")
            raise