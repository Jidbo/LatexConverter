#!/bin/bash
source venv/bin/activate
gunicorn -b 0.0.0.0:5000 "app:create_app('production')"
