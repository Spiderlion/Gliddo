from database import Base
from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime

class ChatMessage(Base):
    """
    Model for storing chat messages in the local interface.
    This model maintains compatibility with the existing database structure
    while providing the necessary fields for chat functionality.
    """
    __tablename__ = 'chat_messages'

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    message_type = Column(String(20))  # 'user' or 'system'
    status = Column(String(20), default='pending')  # 'pending', 'processed', 'responded'

    def to_dict(self):
        """
        Convert the message to a dictionary format for API responses
        """
        return {
            'id': self.id,
            'content': self.content,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'message_type': self.message_type,
            'status': self.status,
        }

    @classmethod
    def create_system_message(cls, content):
        """
        Create a new system-generated message
        """
        return cls(
            content=content,
            message_type='system',
            status='pending'
        )

    @classmethod
    def create_user_message(cls, content):
        """
        Create a new user message
        """
        return cls(
            content=content,
            message_type='user',
            status='pending'
        )
