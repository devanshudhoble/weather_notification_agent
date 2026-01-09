import os
import requests
import smtplib
import schedule
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from datetime import datetime

# ADK Framework Imports
from google.adk.agents import Agent

# Load environment variables
load_dotenv()

# Recipients configuration
RECIPIENTS = [
    {"email": "devanshudhoble32@gmail.com", "name": "Devanshu", "city": "Nagpur"},
    {"email": "devanshudhoble32@gmail.com", "name": "Devanshu", "city": "Bangalore"},
]


def fetch_weather(city: str) -> dict:
    """Fetch weather data from wttr.in (No API key required)."""
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            return get_mock_fallback(city, "Service busy")

        data = response.json()
        current = data['current_condition'][0]
        
        return {
            "success": True,
            "city": city,
            "temperature": float(current['temp_C']),
            "feels_like": float(current['FeelsLikeC']),
            "humidity": int(current['humidity']),
            "condition": current['weatherDesc'][0]['value'],
            "description": current['weatherDesc'][0]['value'],
            "wind_speed": float(current['windspeedKmph']),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "data_source": "wttr.in (Live)",
            "advisory": generate_advisory(float(current['temp_C']), current['weatherDesc'][0]['value'], int(current['humidity']))
        }
    except Exception as e:
        return get_mock_fallback(city, str(e))


def get_mock_fallback(city: str, reason: str) -> dict:
    """Fallback if weather service fails."""
    return {
        "success": True,
        "city": city,
        "temperature": 25.0,
        "feels_like": 26.0,
        "humidity": 60,
        "condition": "Fallback Mode",
        "description": "System operational (Fallback)",
        "wind_speed": 10.0,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "data_source": f"Backup ({reason})",
        "advisory": "✅ Backup data shown."
    }


def generate_advisory(temp, condition, humidity) -> str:
    """Generate simple advisory."""
    advisories = []
    condition = condition.lower()
    
    if temp >= 40: advisories.append("🔥 Extreme heat warning!")
    elif temp >= 35: advisories.append("☀️ Stay hydrated.")
    elif temp <= 10: advisories.append("❄️ Wear warm clothes.")
    
    if "rain" in condition: advisories.append("🌧️ Rain alert.")
    elif "storm" in condition: advisories.append("⛈️ Storm alert.")
    
    return " ".join(advisories) if advisories else "✅ Conditions normal."


def send_email(to_email: str, subject: str, body: str) -> dict:
    """
    Send email via SMTP if configured, else log to file.
    """
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")
    
    # Check if SMTP is configured
    if smtp_email and smtp_password and smtp_password != "your_app_password_here":
        try:
            msg = MIMEMultipart()
            msg["From"] = smtp_email
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))
            
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(smtp_email, smtp_password)
                server.sendmail(smtp_email, to_email, msg.as_string())
            
            return {"success": True, "method": "SMTP", "recipient": to_email}
            
        except Exception as e:
            # Fallback to file logging if SMTP fails
            log_error = f"SMTP Error: {str(e)}"
            return log_email_to_file(to_email, subject, body, error=log_error)
    else:
        # No SMTP configured - Use File Logging Mock
        return log_email_to_file(to_email, subject, body, error="SMTP Credentials missing")


def log_email_to_file(to_email: str, subject: str, body: str, error: str = "") -> dict:
    """Log email to a file when SMTP is unavailable."""
    log_entry = f"""
======================================================================
TIMESTAMP: {datetime.now()}
TO: {to_email}
SUBJECT: {subject}
METHOD: Local File Log (Simulated Email)
NOTE: {error}
----------------------------------------------------------------------
{body}
======================================================================
"""
    try:
        with open("sent_emails.log", "a", encoding="utf-8") as f:
            f.write(log_entry)
        return {"success": True, "method": "File Log", "recipient": to_email, "note": "Check sent_emails.log"}
    except Exception as e:
        return {"success": False, "error": f"Failed to log email: {str(e)}"}


def process_notifications():
    """Worker function to fetch weather and send emails."""
    print(f"[{datetime.now()}] 🔄 Running scheduled weather check...")
    
    results = []
    for recipient in RECIPIENTS:
        weather = fetch_weather(recipient["city"])
        
        subject = f"🌤️ Weather: {weather['city']} - {weather['temperature']}°C | {weather['condition']}"
        
        body = f"""
Dear {recipient['name']},

Here is the weather update for {weather['city']}:

Temp: {weather['temperature']}°C (Feels like {weather['feels_like']}°C)
Condition: {weather['description']}
Humidity: {weather['humidity']}%
Wind: {weather['wind_speed']} km/h
Source: {weather['data_source']}

Advisory: {weather['advisory']}

Best,
Weather Agent
"""
        # Send (or log) the email
        result = send_email(recipient["email"], subject, body)
        results.append(result)
        print(f"   👉 processed {recipient['city']}: {result['method']}")
        
    print(f"[{datetime.now()}] ✅ Job complete.\n")
    return results


def start_scheduler(interval_seconds: int = 21600): # Default 6 hours
    """Start the blocking scheduler."""
    print(f"⏱️  Scheduler started! Running every {interval_seconds} seconds.")
    print("Use Ctrl+C to stop.")
    
    # Run once immediately
    process_notifications()
    
    # Schedule future runs
    schedule.every(interval_seconds).seconds.do(process_notifications)
    
    while True:
        schedule.run_pending()
        time.sleep(1)


def send_weather_to_recipient(city: str, email: str, name: str = "User") -> str:
    """
    Fetch weather for a specific city and send/log email to the specified recipient.
    Useful for ad-hoc requests via chat.
    
    Args:
        city: City name to fetch weather for
        email: Recipient's email address
        name: Recipient's name (optional)
    """
    weather = fetch_weather(city)
    
    subject = f"🌤️ Weather: {weather['city']} - {weather['temperature']}°C | {weather['condition']}"
    
    body = f"""
Dear {name},

Here is the weather update for {weather['city']}:

Temp: {weather['temperature']}°C (Feels like {weather['feels_like']}°C)
Condition: {weather['description']}
Humidity: {weather['humidity']}%
Wind: {weather['wind_speed']} km/h
Source: {weather['data_source']}

Advisory: {weather['advisory']}

Best,
Weather Agent
"""
    
    result = send_email(email, subject, body)
    
    if result.get("success"):
        return f"✅ Weather report for {city} sent to {email} ({result.get('method')})"
    else:
        return f"❌ Failed to send: {result.get('error')}"

if __name__ == "__main__":
    # Test run
    process_notifications()
