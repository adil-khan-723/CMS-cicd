#!/usr/bin/env python
"""
Test script to debug Django admin login issues
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cms_backend.settings')
django.setup()

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

def test_authentication():
    print("🔍 Testing Django Admin Authentication...")
    print("=" * 50)
    
    # Test 1: Direct authentication
    print("1. Testing direct authentication:")
    user = authenticate(username='oggy', password='OGGYOGGY')
    print(f"   Result: {'✅ SUCCESS' if user else '❌ FAILED'}")
    
    user2 = authenticate(username='admin', password='admin123')
    print(f"   Admin Result: {'✅ SUCCESS' if user2 else '❌ FAILED'}")
    
    # Test 2: User permissions
    print("\n2. Testing user permissions:")
    try:
        oggy_user = User.objects.get(username='oggy')
        print(f"   oggy - is_active: {oggy_user.is_active}")
        print(f"   oggy - is_staff: {oggy_user.is_staff}")
        print(f"   oggy - is_superuser: {oggy_user.is_superuser}")
        print(f"   oggy - has_usable_password: {oggy_user.has_usable_password()}")
    except User.DoesNotExist:
        print("   ❌ User 'oggy' not found")
    
    # Test 3: Admin URL access
    print("\n3. Testing admin login via test client:")
    client = Client()
    
    # Get login page
    login_url = reverse('admin:login')
    response = client.get(login_url)
    print(f"   Login page status: {response.status_code}")
    
    # Try to login
    login_data = {
        'username': 'oggy',
        'password': 'OGGYOGGY',
        'next': '/admin/',
    }
    
    # Get CSRF token from the login form
    csrf_token = None
    if 'csrfmiddlewaretoken' in response.context:
        csrf_token = response.context['csrfmiddlewaretoken']
    else:
        # Try to extract from content
        import re
        csrf_match = re.search(r'name=["\']csrfmiddlewaretoken["\'] value=["\']([^"\']+)["\']', response.content.decode())
        if csrf_match:
            csrf_token = csrf_match.group(1)
    
    if csrf_token:
        login_data['csrfmiddlewaretoken'] = csrf_token
    
    response = client.post(login_url, login_data)
    print(f"   Login POST status: {response.status_code}")
    print(f"   Redirect location: {response.get('Location', 'No redirect')}")
    
    if response.status_code == 302 and '/admin/' in response.get('Location', ''):
        print("   ✅ Login appears successful!")
    else:
        print("   ❌ Login failed")
        if hasattr(response, 'context') and response.context:
            form = response.context.get('form')
            if form and hasattr(form, 'errors'):
                print(f"   Form errors: {form.errors}")

if __name__ == '__main__':
    test_authentication()