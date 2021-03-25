#!/bin/bash

export $(less .env)
python manage.py start_tg_admin_bot