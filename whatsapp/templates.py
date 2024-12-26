# templates.py

from typing import Dict, Any
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MessageTemplates:
    """
    Handles storage and retrieval of WhatsApp message templates.
    Templates are organized by category and type for easy access and maintenance.
    """
    
    def __init__(self):
        # Initialize with default templates
        self.templates = {
            "daily_updates": {
                "morning": """
Good morning! 🌅

Here's your daily task checklist:
1️⃣ Update your completed tasks
2️⃣ Share any challenges
3️⃣ List tomorrow's planned tasks

Reply with your updates! 💪
                """.strip(),
                
                "reminder": """
Friendly reminder! ⏰
We're waiting for your daily update.
Takes just 2 minutes to share your progress!
                """.strip()
            },
            
            "feedback": {
                "positive": """
Great work today! 🌟
Your updates show excellent progress.
Keep up the momentum!

Key highlights:
{highlights}
                """.strip(),
                
                "improvement": """
Thank you for your update! 📝

A few points to consider:
{improvement_points}

Let me know if you need any support!
                """.strip()
            },
            
            "reports": {
                "weekly": """
📊 Weekly Performance Summary
Week: {week_range}
───────────────

✅ Completion Rate: {completion_rate}%
⭐ Quality Score: {quality_score}/10

🎯 Top Achievements:
{achievements}

💡 Focus Areas:
{focus_areas}
                """.strip()
            }
        }
    
    def get_template(self, category: str, template_type: str, **kwargs) -> str:
        """
        Retrieve and format a specific template with provided parameters.
        
        Args:
            category: The template category (e.g., 'daily_updates')
            template_type: The specific template type (e.g., 'morning')
            **kwargs: Variables to format the template with
            
        Returns:
            Formatted template string
        """
        try:
            template = self.templates[category][template_type]
            return template.format(**kwargs) if kwargs else template
        except KeyError:
            logger.error(f"Template not found: {category}/{template_type}")
            return "Template not found. Please check the category and type."
        except Exception as e:
            logger.error(f"Error formatting template: {str(e)}")
            return "Error formatting template. Please check the parameters."

    def add_template(self, category: str, template_type: str, template: str) -> bool:
        """
        Add a new template or update existing one.
        
        Args:
            category: Template category
            template_type: Template type
            template: The template string
            
        Returns:
            bool: Success status
        """
        try:
            if category not in self.templates:
                self.templates[category] = {}
            self.templates[category][template_type] = template.strip()
            return True
        except Exception as e:
            logger.error(f"Error adding template: {str(e)}")
            return False

    def save_to_file(self, filepath: str) -> bool:
        """Save templates to a JSON file for persistence"""
        try:
            with open(filepath, 'w') as f:
                json.dump(self.templates, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving templates: {str(e)}")
            return False

    def load_from_file(self, filepath: str) -> bool:
        """Load templates from a JSON file"""
        try:
            with open(filepath, 'r') as f:
                self.templates = json.load(f)
            return True
        except Exception as e:
            logger.error(f"Error loading templates: {str(e)}")
            return False