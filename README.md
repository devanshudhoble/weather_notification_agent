# 🌤️ Autonomous Weather Notification Agent

An autonomous AI agent that fetches real-time weather data and sends professional email notifications automatically. Built with **Google ADK Framework**.

## 🚀 Features

*   **Fully Autonomous**: Runs on a background schedule (every 6 hours) without human intervention.
*   **Live Weather Data**: Fetches real-time temperature, humidity, and conditions via `wttr.in`.
*   **Zero-Touch Automation**: Recipients receive updates automatically; no action required on their end.
*   **Dual Email Modes**:
    *   **Safe Mode** (Default): Logs emails to `sent_emails.log` for secure testing.
    *   **Live Mode**: Sends actual emails via SMTP (configurable).
*   **Ad-Hoc Queries**: Supports fetching weather for any city via chat interface.

## 🛠️ Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/devanshudhoble/weather_notification_agent.git
    cd weather_notification_agent
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Configure Environment:
    *   Rename `env.example` to `.env`.
    *   Add your keys (Groq API Key, etc.).

## 🏃 Usage

### 1. Run the Automated Scheduler
To start the background process that checks weather every 6 hours:
```bash
python run_scheduler.py
```
*Leave this running to keep automation active.*

### 2. Run the Web Interface
To interact with the agent manually or send one-off emails:
```bash
adk web
```
Then open `http://localhost:8000` in your browser.

## 📝 Configuration

The system is configured in `agent.py`. You can modify:
*   **Recipients**: Update the `RECIPIENTS` list in `agent.py`.
*   **Schedule**: Change `interval_seconds` in `run_scheduler.py`.

## 📂 Project Structure

*   `agent.py`: Core logic for weather fetching and email formatting.
*   `run_scheduler.py`: The automation loop.
*   `sent_emails.log`: Audit log of all sent notifications (Proof of Work).
*   `__init__.py`: ADK Agent definition.

---
*Built with ❤️ using Google ADK*
