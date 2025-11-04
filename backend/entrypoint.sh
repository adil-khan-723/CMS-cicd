#!/bin/sh
set -e

python manage.py migrate --noinput

# Ensure a superuser exists (uses env vars)
python - <<'PY'
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cms_backend.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
if username and password:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print('Superuser created:', username)
    else:
        print('Superuser already exists:', username)
else:
    print('DJANGO_SUPERUSER_* not fully set; skipping superuser creation')
PY

python manage.py runserver 0.0.0.0:8000
