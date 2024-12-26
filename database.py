from dotenv import load_dotenv
import os
from supabase import create_client, Client
import logging
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Supabase Session Pooler connection URL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres.rdjxfeltmixaxbfqcngb:Ravindra%409205959919@aws-0-ap-south-1.pooler.supabase.com:5432/postgres?sslmode=require"

# Create the engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SupabaseManager:
    def __init__(self):
        """Initialize Supabase connection"""
        load_dotenv()
        
        # Load environment variables
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        
        if not all([self.supabase_url, self.supabase_key]):
            raise ValueError("Missing required environment variables for Supabase")
        
        # Initialize Supabase client
        self.client: Client = create_client(self.supabase_url, self.supabase_key)
        
    async def create_employee(self, name: str, whatsapp_number: str) -> Dict[str, Any]:
        """Create a new employee record"""
        try:
            data = {
                "name": name,
                "whatsapp_number": whatsapp_number,
                "status": "active",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "last_active": datetime.now(timezone.utc).isoformat()
            }
            
            result = self.client.table("employees").insert(data).execute()
            logger.info(f"Created employee record for {name}")
            return result.data[0]
            
        except Exception as e:
            logger.error(f"Error creating employee: {str(e)}")
            raise
            
    async def get_employee(self, employee_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve employee details by ID"""
        try:
            result = self.client.table("employees").select("*").eq("id", employee_id).execute()
            return result.data[0] if result.data else None
            
        except Exception as e:
            logger.error(f"Error retrieving employee {employee_id}: {str(e)}")
            raise
            
    async def update_employee_status(self, employee_id: str, status: str) -> Dict[str, Any]:
        """Update employee status"""
        try:
            data = {
                "status": status,
                "last_active": datetime.now(timezone.utc).isoformat()
            }
            
            result = self.client.table("employees").update(data).eq("id", employee_id).execute()
            logger.info(f"Updated status for employee {employee_id}")
            return result.data[0]
            
        except Exception as e:
            logger.error(f"Error updating employee status: {str(e)}")
            raise
            
    async def create_daily_task(self, employee_id: str, tasks_planned: str) -> Dict[str, Any]:
        """Create a daily task record"""
        try:
            data = {
                "employee_id": employee_id,
                "task_date": datetime.now(timezone.utc).date().isoformat(),
                "tasks_planned": tasks_planned,
                "status": "pending",
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            
            result = self.client.table("daily_tasks").insert(data).execute()
            logger.info(f"Created daily task record for employee {employee_id}")
            return result.data[0]
            
        except Exception as e:
            logger.error(f"Error creating daily task: {str(e)}")
            raise
            
    async def log_message(self, employee_id: str, message_type: str, 
                         content: str, attempt_number: int = 1) -> Dict[str, Any]:
        """Log a message sent to an employee"""
        try:
            data = {
                "employee_id": employee_id,
                "message_type": message_type,
                "message_content": content,
                "sent_at": datetime.now(timezone.utc).isoformat(),
                "attempt_number": attempt_number
            }
            
            result = self.client.table("message_logs").insert(data).execute()
            logger.info(f"Logged message for employee {employee_id}")
            return result.data[0]
            
        except Exception as e:
            logger.error(f"Error logging message: {str(e)}")
            raise
            
    async def update_message_response(self, message_id: str, 
                                    response: str) -> Dict[str, Any]:
        """Update message record with employee response"""
        try:
            data = {
                "response": response,
                "response_time": datetime.now(timezone.utc).isoformat()
            }
            
            result = self.client.table("message_logs").update(data).eq("id", message_id).execute()
            logger.info(f"Updated message response for message {message_id}")
            return result.data[0]
            
        except Exception as e:
            logger.error(f"Error updating message response: {str(e)}")
            raise

    async def get_employee_history(self, employee_id: str) -> List[Dict[str, Any]]:
        """Get employee's historical task and performance data"""
        try:
            result = self.client.table("daily_tasks")\
                .select("*")\
                .eq("employee_id", employee_id)\
                .order("created_at", desc=True)\
                .limit(10)\
                .execute()
            return result.data
        except Exception as e:
            logger.error(f"Error getting employee history: {str(e)}")
            raise

    async def create_feedback_record(self, 
                               employee_id: str, 
                               feedback_content: str,
                               created_at: str) -> Dict[str, Any]:
        """Store feedback records in the database"""
        try:
            data = {
                "employee_id": employee_id,
                "feedback_content": feedback_content,
                "created_at": created_at
            }
            
            result = self.client.table("feedback_records").insert(data).execute()
            return result.data[0]
        except Exception as e:
            logger.error(f"Error creating feedback record: {str(e)}")
            raise
