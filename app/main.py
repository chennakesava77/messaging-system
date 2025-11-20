from fastapi import FastAPI, Query
from typing import Optional
from app.tasks import send_email_task, log_time_task

app = FastAPI()

# --- NEW ROOT ENDPOINT ---
@app.get("/")
def root():
    return {"message": "FastAPI server is running!"}
@app.get("/messages")
def get_messages():
    return {"messages": ["Hello", "Hi", "Welcome"]}

@app.get("/users")
def get_users():
    return {"users": ["Alice", "Bob", "Kesava"]}

# --- HEALTH CHECK ---
@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

# --- ACTION ENDPOINT ---
@app.get("/action")
async def action(
    sendmail: Optional[str] = Query(None, description="Email address to send mail to"),
    talktome: Optional[bool] = Query(None, description="Trigger a log time task")
):
    """
    Queue background tasks based on query parameters.
    - If `sendmail` is provided, queue an email task.
    - If `talktome` is True, queue a log time task.
    """
    if sendmail:
        send_email_task.delay(sendmail)
        return {
            "status": "success",
            "message": f"Email task queued for {sendmail}"
        }

    if talktome:
        log_time_task.delay()
        return {
            "status": "success",
            "message": "Time logged"
        }

    return {
        "status": "error",
        "message": "Invalid request. Provide ?sendmail= or ?talktome=true"
    }
