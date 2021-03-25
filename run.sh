#!/bin/bash

export $(less .env)
gunicorn --bind 0.0.0.0:8080 project.wsgi
