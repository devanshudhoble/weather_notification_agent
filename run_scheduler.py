"""
Script to start the Weather Notification Scheduler.
Run this in a separate terminal to keep the automation active.
"""

from agent import start_scheduler

if __name__ == "__main__":
    # Start scheduler running every 6 hours (21600 seconds)
    # For testing, you can change this to 60 seconds
    start_scheduler(interval_seconds=21600)
