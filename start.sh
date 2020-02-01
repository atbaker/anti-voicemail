#!/bin/bash
# Start script for Party Line

# Set some environment variables
export PYTHONUNBUFFERED=true

# Start the app
gunicorn --bind=localhost:5000 --log-level debug anti_voicemail:app
