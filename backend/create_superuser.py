#!/usr/bin/env python
"""
Script to create Django superuser with predefined credentials.
Run this after setting up Django environment.
"""

import os
import sys
import django

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cms_backend.settings')

# Setup Django
django.setup()

from django.contrib.auth import get_user_model

def create_superuser():
    User = get_user_model()
    
    username = 'oggy'
    password = 'OGGYOGGY'
    email = 'oggy@example.com'  # Optional email
    
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        print(f"❌ User '{username}' already exists!")
        return
    
    # Create superuser
    try:
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"✅ Superuser '{username}' created successfully!")
        print(f"Username: {username}")
        print(f"Password: {password}")
        print(f"Email: {email}")
        print(f"Admin URL: http://127.0.0.1:8000/admin/")
        
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")

if __name__ == '__main__':
    create_superuser()