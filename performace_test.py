from performance_analyzer import PerformanceAnalyzer
import asyncio

async def test_performance_analysis():
    analyzer = PerformanceAnalyzer()
    
    # Test task completion analysis
    task_data = {
        "tasks_planned": "Task 1\nTask 2\nTask 3",
        "tasks_completed": "Task 1\nTask 2\nExtra Task"
    }
    completion_metrics = await analyzer.analyze_task_completion(
        "bf615338-8a52-450e-ba5d-5ac172936d93",
        task_data
    )
    print("Completion Metrics:", completion_metrics)
    
    # Generate insights
    insights = await analyzer.generate_insights("bf615338-8a52-450e-ba5d-5ac172936d93")
    print("Performance Insights:", insights)

if __name__ == "__main__":
    asyncio.run(test_performance_analysis())