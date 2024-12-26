# main.py
import os
import logging
import asyncio
from dotenv import load_dotenv

# Example imports -- adjust as needed for your project
from enhanced_data_manager import EnhancedDataManager
from whatsapp.templates import MessageTemplates
from whatsapp.dynamic_templates import DynamicTemplateGenerator

# 1. Set up logging so INFO-level messages are shown in the console
logging.basicConfig(level=logging.INFO)

# 2. Load env variables if you're using .env
load_dotenv()

async def main():
    # Check if we can see this print statement (sanity check)
    print("Starting the main() function...")

    # Example: Use EnhancedDataManager
    manager = EnhancedDataManager()
    
    # Store some test analysis
    analysis = await manager.store_task_analysis(
        "bf615338-8a52-450e-ba5d-5ac172936d93",
        {"completion_rate": 85, "quality_score": 90}
    )
    print("Stored analysis:", analysis)
    
    # Get recent interactions
    interactions = await manager.get_recent_interactions("bf615338-8a52-450e-ba5d-5ac172936d93")
    print("Recent interactions:", interactions)

    # 3. Demonstrate usage of template classes
    templates = MessageTemplates()
    dynamic_gen = DynamicTemplateGenerator()

    # Get a basic (static) template
    morning_template = templates.get_template("daily_updates", "morning")
    print("Morning template:", morning_template)

    # 4. Actually call the dynamic generator and print the result
    personalized_message = await dynamic_gen.generate_personalized_message(
        "bf615338-8a52-450e-ba5d-5ac172936d93",  # Must be a UUID if your DB expects it
        "daily_updates/morning"
    )
    print("Personalized message:", personalized_message)

if __name__ == "__main__":
    asyncio.run(main())