import psycopg2
import os
from datetime import datetime
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class EnhancedDataManager:
    def __init__(self):
        """
        Initialize the database connection
        """
        self.conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "postgres"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT", "5432")  # Default to PostgreSQL port
        )
        self.cursor = self.conn.cursor()

    def close_connection(self):
        """
        Close the database connection
        """
        self.cursor.close()
        self.conn.close()

    async def store_task_analysis(self, employee_id, analysis_data):
        try:
            query = """
                INSERT INTO task_analysis (employee_id, analysis_data, created_at)
                VALUES (%s, %s, %s)
                RETURNING id;
            """
            self.cursor.execute(query, (employee_id, analysis_data, datetime.utcnow()))
            self.conn.commit()
            return self.cursor.fetchone()
        except Exception as e:
            logger.error(f"Error storing task analysis: {e}")
            return None

    async def get_recent_interactions(self, employee_id):
        try:
            query = """
                SELECT * FROM message_logs
                WHERE employee_id = %s
                ORDER BY sent_at DESC
                LIMIT 10;
            """
            self.cursor.execute(query, (employee_id,))
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Error fetching recent interactions: {e}")
            return None

    async def log_message(self, employee_id, message_type, content, attempt_number=1):
        try:
            query = """
                INSERT INTO message_logs (employee_id, message_type, message_content, sent_at, attempt_number)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
            """
            self.cursor.execute(query, (employee_id, message_type, content, datetime.utcnow(), attempt_number))
            self.conn.commit()
            return self.cursor.fetchone()
        except Exception as e:
            logger.error(f"Error logging message: {e}")
            return None

    async def update_message_response(self, message_id, response):
        try:
            query = """
                UPDATE message_logs
                SET response = %s, response_time = %s
                WHERE id = %s
                RETURNING id;
            """
            self.cursor.execute(query, (response, datetime.utcnow(), message_id))
            self.conn.commit()
            return self.cursor.fetchone()
        except Exception as e:
            logger.error(f"Error updating message response: {e}")
            return None

    async def create_daily_task(self, employee_id, tasks_planned):
        try:
            query = """
                INSERT INTO daily_tasks (employee_id, task_date, tasks_planned, status, created_at)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
            """
            self.cursor.execute(query, (employee_id, datetime.utcnow().date(), tasks_planned, "pending", datetime.utcnow()))
            self.conn.commit()
            return self.cursor.fetchone()
        except Exception as e:
            logger.error(f"Error creating daily task: {e}")
            return None

    async def get_employee_history(self, employee_id):
        try:
            query = """
                SELECT * FROM daily_tasks
                WHERE employee_id = %s
                ORDER BY created_at DESC
                LIMIT 10;
            """
            self.cursor.execute(query, (employee_id,))
            return self.cursor.fetchall()
        except Exception as e:
            logger.error(f"Error getting employee history: {e}")
            return None

    async def create_feedback_record(self, employee_id, feedback_content):
        try:
            query = """
                INSERT INTO feedback_records (employee_id, feedback_content, created_at)
                VALUES (%s, %s, %s)
                RETURNING id;
            """
            self.cursor.execute(query, (employee_id, feedback_content, datetime.utcnow()))
            self.conn.commit()
            return self.cursor.fetchone()
        except Exception as e:
            logger.error(f"Error creating feedback record: {e}")
            return None
