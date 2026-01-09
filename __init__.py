"""
Weather Notification Agent - ADK Powered
Autonomous agent for Bangalore and Nagpur weather notifications.

Powered by Google ADK Framework.
"""

# IMPORTING ADK FRAMEWORK
from google.adk.agents import Agent
from .agent import fetch_weather, get_weather_notification, run_weather_notifications, send_weather_to_recipient

# Agent definition using Google ADK
root_agent = Agent(
    name="weather_notification_agent",
    model="groq/llama-3.3-70b-versatile",
    description="Autonomous Weather Notification Agent using Google ADK",
    instruction="""You are an autonomous Weather Notification Agent powered by Google ADK.

Your primary mission:
1. Fetch live weather data for Bangalore and Nagpur.
2. Format and display professional weather reports.

ACTIONS:
- When asked about weather, use `get_weather_notification`.
- To run the daily cycle for all, use `run_weather_notifications`.
- **To send a weather email to a specific person**, use `send_weather_to_recipient`.
  Example: "Send weather for London to user@example.com"

You have access to immediate weather data via wttr.in integration.
""",
    tools=[fetch_weather, get_weather_notification, run_weather_notifications, send_weather_to_recipient],
)
