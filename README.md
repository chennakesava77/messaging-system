# messaging-system
# Messaging System with RabbitMQ, Celery, Nginx, and Python

## Project Overview
This project implements a simple messaging system demonstrating **asynchronous task processing** using **RabbitMQ** as a message broker and **Celery** as a task queue. A lightweight Python web application is served behind **Nginx**, providing endpoints for sending emails asynchronously and logging the current time. The system can be exposed externally using **ngrok** for testing.

---

## Table of Contents
- [Objective](#objective)  
- [System Architecture](#system-architecture)  
- [Functional Requirements](#functional-requirements)  
- [Implementation Steps](#implementation-steps)  
- [Testing Procedure](#testing-procedure)  
- [Technologies Used](#technologies-used)  
- [Deliverables](#deliverables)  
- [Conclusion](#conclusion)  

---

## Objective
The goal of this project is to build a messaging system that:  
- Demonstrates **asynchronous task execution** via Celery and RabbitMQ.  
- Provides **email sending** and **time logging** functionalities.  
- Uses Nginx for **reverse proxy** and exposes the service publicly via ngrok.

---

## System Architecture
[ Client ] ---> [ Nginx Reverse Proxy ] ---> [ Python App (Flask/FastAPI) ]-->[ Celery Worker ] <---> [ RabbitMQ ]

1. **Frontend (Nginx Reverse Proxy)**  
   - Listens on port 80.  
   - Routes HTTP requests to the Python web application (Gunicorn/Uvicorn).  

2. **Backend (Python Application)**  
   - Flask or FastAPI application with two endpoints:  
     - `/action?sendmail=<recipient_email>` → Sends email asynchronously via Celery.  
     - `/action?talktome` → Logs the current server time synchronously.  

3. **Task Queue (Celery + RabbitMQ)**  
   - RabbitMQ acts as the message broker.  
   - Celery workers process tasks in the background:  
     - `send_email_task` → Sends email.  
     - `log_time_task` → Logs current time (can also be asynchronous).  

4. **External Exposure (Ngrok)**  
   - Exposes local Nginx server to a public HTTPS endpoint.  
   - Allows external testing of email and logging endpoints.

---

## Functional Requirements

### 1. Email Sending (`?sendmail`)
- Accepts an email address as a query parameter.  
- Publishes a "send email" task to RabbitMQ.  
- Celery worker sends email asynchronously via SMTP.

### 2. Logging Time (`?talktome`)
- Logs the current server timestamp into `app.log`.  
- Demonstrates synchronous logging; can be adapted to a Celery task.

### 3. Task Execution
- Email sending is **asynchronous**.  
- Logging can be synchronous or asynchronous depending on configuration.

---

## Implementation Steps

### 1. Install Dependencies
```bash
# Python packages
pip install fastapi celery uvicorn flask gunicorn

# System packages
sudo apt install rabbitmq-server nginx
2.Setup RabbitMQ:
# Start RabbitMQ
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server
3. Configure Celery

Define Celery tasks (send_email_task, log_time_task) in a tasks.py file.

Configure broker URL to point to RabbitMQ.

4. Develop Python Application

Flask or FastAPI routes:

/action?sendmail=<email>
/action?talktome


Routes call Celery tasks as required.

5. Configure SMTP for Email

Use environment variables for SMTP credentials.

Test email sending with Celery worker.

6. Deploy Behind Nginx

Configure reverse proxy from Nginx to Gunicorn/Uvicorn.

Example Nginx config:

server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

7. Expose Public Endpoint

Use ngrok to expose local Nginx server:

ngrok http 80

Testing Procedure

Access endpoints via ngrok public URL:

Email: https://<ngrok-id>.ngrok.io/action?sendmail=test@your mail@gmail.com

Expected: Email sent asynchronously.

Logging: https://<ngrok-id>.ngrok.io/action?talktome

Expected: Current timestamp appended to app.log.

**Verify:-

RabbitMQ is running locally.

Celery workers are processing tasks.

Flask/FastAPI responds correctly via Nginx.

**Technologies Used:-

RabbitMQ – Message broker

Celery – Asynchronous task queue manager

Flask / FastAPI – Python web framework

Gunicorn / Uvicorn – Application server

Nginx – Reverse proxy

SMTP – Email sending

Ngrok – Public exposure for testing

Python 3.9+

**Deliverables:

Working messaging system exposed via ngrok.

Screen recording (≤ 3 minutes) showing:

RabbitMQ running locally.

Celery workers retrieving tasks.

Flask/Nginx responding to requests.

Email successfully sent.

Log file updated with timestamps.

Ngrok public endpoint demonstration.

**Conclusion:-

This project demonstrates a production-like asynchronous messaging system with:

Task queuing via Celery + RabbitMQ.

Background job execution.

Reverse proxying with Nginx.

External access via ngrok for testing.
It serves as a foundational example for building scalable and asynchronous Python applications.



