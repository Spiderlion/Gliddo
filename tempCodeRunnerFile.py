import json
import logging

import openai


async def analyze_communication_quality(self, response_text: str) -> dict[str, any]:
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
