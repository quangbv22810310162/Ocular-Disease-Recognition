"""WSGI entry point for production servers like Gunicorn or Waitress."""
import os

from app import app, init_db

if os.getenv('INIT_DB_ON_STARTUP', 'true').lower() == 'true':
    init_db()

application = app
