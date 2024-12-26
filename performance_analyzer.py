from typing import Dict, List, Any, Optional
from datetime import datetime, timezone, timedelta
import logging
from enhanced_data_manager import EnhancedDataManager
import openai
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerformanceAnalyzer:
    def __init__(self):
        load_dotenv()
        self.data_manager = EnhancedDataManager()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
    async def analyze_task_completion(self, 
                                    employee_id: str,
                                    task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze task completion status and quality"""
        try:
            planned_tasks = set(task_data.get('tasks_planned', '').split('\n'))
            completed_tasks = set(task_data.get('tasks_completed', '').split('\n'))
            
            completion_metrics = {
                'total_planned': len(planned_tasks),
                'total_completed': len(completed_tasks),
                'completion_rate': len(completed_tasks) / len(planned_tasks) if planned_tasks else 0,
                'incomplete_tasks': list(planned_tasks - completed_tasks),
                'additional_tasks': list(completed_tasks - planned_tasks),
                'on_track': len(completed_tasks) >= len(planned_tasks) * 0.8
            }
            
            return completion_metrics
        except Exception as e:
            logger.error(f"Error in analyze_task_completion: {e}")
            return {
                'total_planned': 0,
                'total_completed': 0,
                'completion_rate': 0,
                'incomplete_tasks': [],
                'additional_tasks': [],
                'on_track': False
            }
            
    async def evaluate_response_quality(self, 
                                      response_text: str,
                                      task_context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate the quality of task responses using GPT-3.5"""
        try:
            prompt = f"""
            Analyze this task response for quality and completeness:
            Task Context: {task_context}
            Response: {response_text}
            
            Evaluate based on:
            1. Completeness (1-10)
            2. Clarity (1-10)
            3. Professional tone (1-10)
            4. Problem-solving approach (1-10)
            
            Return evaluation as JSON with scores and specific feedback for improvement.
            """
            
            response = await openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            
            evaluation = response.choices[0].message.content
            return evaluation
        except Exception as e:
            logger.error(f"Error in evaluate_response_quality: {e}")
            return {
                'error': 'Unable to evaluate response quality',
                'details': str(e)
            }
            
    async def generate_insights(self,
                              employee_id: str,
                              time_period: str = "1w") -> Dict[str, Any]:
        """Generate actionable insights based on performance data"""
        try:
            # Calculate date range
            end_date = datetime.now(timezone.utc)
            if time_period == "1w":
                start_date = end_date - timedelta(days=7)
            elif time_period == "1m":
                start_date = end_date - timedelta(days=30)
            
            # Get historical data
            history = await self.data_manager.get_employee_performance_history(
                employee_id,
                start_date.date().isoformat(),
                end_date.date().isoformat()
            )
            
            # Analyze trends
            completion_rates = []
            response_qualities = []
            task_patterns = {}
            
            for entry in history:
                try:
                    metrics = await self.analyze_task_completion(employee_id, entry)
                    completion_rates.append(metrics['completion_rate'])

                    quality = await self.evaluate_response_quality(
                        entry.get('tasks_completed', ''),
                        {'date': entry['task_date']}
                    )
                    response_qualities.append(quality)
                    
                    # Track task patterns
                    for task in entry.get('tasks_completed', '').split('\n'):
                        task_patterns[task] = task_patterns.get(task, 0) + 1
                except Exception as e:
                    logger.error(f"Error processing entry {entry}: {e}")
                    continue
            
            # Generate insights
            insights = {
                'performance_trend': {
                    'completion_rate_trend': sum(completion_rates) / len(completion_rates) if completion_rates else 0,
                    'quality_trend': response_qualities,
                    'trend_direction': 'improving' if completion_rates and completion_rates[-1] > completion_rates[0] else 'declining'
                },
                'common_tasks': sorted(task_patterns.items(), key=lambda x: x[1], reverse=True)[:5],
                'recommendations': await self._generate_recommendations(
                    completion_rates,
                    response_qualities,
                    task_patterns
                )
            }
            
            # Store insights
            await self.data_manager.store_ai_feedback(
                employee_id,
                'performance_insights',
                insights
            )
            
            return insights
        except Exception as e:
            logger.error(f"Error in generate_insights: {e}")
            return {
                'performance_trend': {},
                'common_tasks': [],
                'recommendations': []
            }
            
    async def _generate_recommendations(self,
                                      completion_rates: List[float],
                                      quality_scores: List[Dict],
                                      task_patterns: Dict[str, int]) -> List[str]:
        """Generate specific recommendations based on performance data"""
        try:
            recommendations = []
            
            # Analyze completion rate trend
            avg_completion = sum(completion_rates) / len(completion_rates) if completion_rates else 0
            if avg_completion < 0.8:
                recommendations.append({
                    'area': 'Task Completion',
                    'observation': 'Below target completion rate',
                    'suggestion': 'Consider breaking down tasks into smaller, manageable chunks'
                })
            
            # Analyze quality trends
            quality_issues = [q for q in quality_scores if q.get('average_score', 0) < 7]
            if quality_issues:
                recommendations.append({
                    'area': 'Response Quality',
                    'observation': 'Quality scores below threshold in some areas',
                    'suggestion': 'Focus on providing more detailed and structured responses'
                })
            
            # Analyze task patterns
            if len(task_patterns) < 3:
                recommendations.append({
                    'area': 'Task Variety',
                    'observation': 'Limited variety in tasks',
                    'suggestion': 'Consider expanding skill set and taking on diverse responsibilities'
                })
                
            return recommendations
        except Exception as e:
            logger.error(f"Error in _generate_recommendations: {e}")
            return []