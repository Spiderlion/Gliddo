from flask import Flask, render_template, request, jsonify
from database import SessionLocal, engine
from chat_models import ChatMessage, Base
from ai_agent import AIAgent
from enhanced_data_manager import EnhancedDataManager
from datetime import datetime
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fetch the OpenAI API key from the .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Initialize Flask application
app = Flask(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize components
ai_agent = AIAgent(openai_api_key=OPENAI_API_KEY)
data_manager = EnhancedDataManager()

def get_db():
    """
    Get a database session
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Error in database session: {e}")
    finally:
        db.close()

@app.route('/')
def chat_interface():
    """
    Render the main chat interface
    """
    try:
        db = next(get_db())
        messages = db.query(ChatMessage).order_by(ChatMessage.timestamp.desc()).limit(50).all()
        return render_template('chat.html', messages=messages)
    except Exception as e:
        logger.error(f"Error rendering chat interface: {e}")
        return "An error occurred while loading the chat interface.", 500

@app.route('/api/send_message', methods=['POST'])
def send_message():
    """
    Handle incoming messages from the user
    """
    try:
        db = next(get_db())
        content = request.json.get('message')
        if not content:
            logger.error("No message content provided.")
            return jsonify({'error': 'Message content is required'}), 400

        # Log the incoming message
        logger.info(f"Received message: {content}")

        # Create user message
        user_message = ChatMessage.create_user_message(content)
        db.add(user_message)
        db.commit()

        # Process with AI agent
        ai_response = ai_agent.process_message(content)
        logger.info(f"AI Response: {ai_response}")

        # Create AI response message
        ai_message = ChatMessage.create_system_message(ai_response)
        db.add(ai_message)
        db.commit()

        return jsonify({
            'user_message': user_message.to_dict(),
            'ai_response': ai_message.to_dict()
        })

    except Exception as e:
        logger.error(f"Error in /api/send_message: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)