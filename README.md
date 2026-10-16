# Enterprise Student Record & Academic Management Platform

A Flask REST service for managing students, courses, enrollments and grades,
delivered through an automated CI/CD pipeline (GitHub, Jenkins, Docker, Kubernetes).

## Run locally

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python run.py

Health check: http://localhost:5000/api/health
