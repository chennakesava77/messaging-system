from celery import Celery
from datetime import datetime
import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Celery
celery = Celery('tasks', broker='pyamqp://guest@localhost//')

@celery.task
def send_email_task(recipient):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")

    msg = EmailMessage()
    msg['Subject'] = 'Test Email from Messaging System'
    msg['From'] = smtp_user
    msg['To'] = recipient
    msg.set_content(f"Hello {recipient},\n\nThis is a test email sent asynchronously via Celery and RabbitMQ.")

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        print(f"[✓] Email sent to {recipient}")
    except Exception as e:
        print(f"[✗] Failed to send email to {recipient}: {e}")

@celery.task
def log_time_task():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open("app.log", "a") as f:
            f.write(f"{timestamp}\n")
        print(f"[✓] Logged time: {timestamp}")
    except Exception as e:
        print(f"[✗] Failed to log time: {e}")