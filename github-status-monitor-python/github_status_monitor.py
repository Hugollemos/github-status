#!/usr/bin/env python3
import os
import json
import time
import requests
import schedule
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
TEAMS_WEBHOOK_URL = os.getenv('TEAMS_WEBHOOK_URL')
GITHUB_STATUS_API_URL = os.getenv('GITHUB_STATUS_API_URL', 'https://www.githubstatus.com/api/v2/summary.json')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 5))

def get_github_status():
    """Fetch current GitHub status from the API."""
    try:
        response = requests.get(GITHUB_STATUS_API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching GitHub status: {e}")
        return None

def create_teams_message(status_data):
    """Create a formatted message for Microsoft Teams."""
    if not status_data:
        return {
            "type": "message",
            "attachments": [{
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "type": "AdaptiveCard",
                    "body": [{
                        "type": "TextBlock",
                        "text": "❌ Error fetching GitHub status",
                        "weight": "bolder",
                        "size": "large"
                    }],
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.0"
                }
            }]
        }

    status = status_data.get('status', {})
    components = status_data.get('components', [])
    
    # Create status summary
    status_text = f"GitHub Status: {status.get('description', 'Unknown')}"
    status_emoji = "🟢" if status.get('indicator') == 'none' else "🔴"
    
    # Create components status
    components_text = "\n\nComponents Status:"
    for component in components:
        name = component.get('name', 'Unknown')
        status = component.get('status', 'unknown')
        emoji = "🟢" if status == 'operational' else "🔴"
        components_text += f"\n{emoji} {name}: {status}"

    return {
        "type": "message",
        "attachments": [{
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "type": "AdaptiveCard",
                "body": [{
                    "type": "TextBlock",
                    "text": f"{status_emoji} {status_text}{components_text}",
                    "weight": "bolder",
                    "size": "medium"
                }],
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "version": "1.0"
            }
        }]
    }

def send_teams_notification(message):
    """Send notification to Microsoft Teams."""
    try:
        response = requests.post(TEAMS_WEBHOOK_URL, json=message)
        response.raise_for_status()
        print("Notification sent successfully")
    except requests.RequestException as e:
        print(f"Error sending Teams notification: {e}")

def check_and_notify():
    """Main function to check GitHub status and send notification if needed."""
    print(f"Checking GitHub status at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    status_data = get_github_status()
    message = create_teams_message(status_data)
    send_teams_notification(message)

def main():
    """Main function to run the monitor."""
    if not TEAMS_WEBHOOK_URL:
        print("Error: TEAMS_WEBHOOK_URL environment variable is not set")
        return

    print(f"Starting GitHub Status Monitor (checking every {CHECK_INTERVAL} minutes)")
    
    # Run immediately on startup
    check_and_notify()
    
    # Schedule regular checks
    schedule.every(CHECK_INTERVAL).minutes.do(check_and_notify)
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main() 