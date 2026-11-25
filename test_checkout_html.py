#!/usr/bin/env python
"""Test to verify the actual checkout page HTML output."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cheran_pumps.settings')
django.setup()

from django.test import RequestFactory, Client
from django.contrib.auth import get_user_model
from accounts.models import User
from orders.views import checkout

# Get or create test user
User_model = get_user_model()
user = User_model.objects.filter(username='testuser').first()
if not user:
    user = User_model.objects.create_user('testuser', 'test@test.com', 'testpass123')
    print(f"Created user: {user.username}")

# Create a request factory
factory = RequestFactory()

# Create a request as if the user is visiting the checkout page
request = factory.get('/orders/checkout/')
request.user = user
request.session = {}

# Render the checkout view
response = checkout(request)

print("=" * 80)
print("CHECKOUT PAGE HTML OUTPUT")
print("=" * 80)

content = response.content.decode('utf-8')

# Extract just the payment method section
import re
payment_section = re.search(r'<label class="form-label fw-bold">Payment Method.*?</div>\s*</div>', content, re.DOTALL)
if payment_section:
    print("\nPAYMENT METHOD SECTION:")
    print("-" * 80)
    print(payment_section.group(0))
    print("-" * 80)

# Check for keywords
print("\n" + "=" * 80)
print("KEYWORD VERIFICATION:")
print("=" * 80)

keywords_to_check = [
    ('upi', 'UPI Payment'),
    ('UPI', 'UPI uppercase'),
    ('razorpay', 'Razorpay'),
    ('Razorpay', 'Razorpay uppercase'),
    ('online', 'Online Payment'),
    ('Online', 'Online uppercase'),
]

for keyword, description in keywords_to_check:
    found = keyword in content
    status = "❌ FOUND" if found else "✅ NOT FOUND"
    print(f"  {status}: '{keyword}' ({description})")

# Check for Cash on Delivery
cod_check = 'Cash on Delivery' in content
print(f"\n  {'✅' if cod_check else '❌'} 'Cash on Delivery' {'FOUND' if cod_check else 'NOT FOUND'}")

# Check for radio buttons
radio_count = content.count('type="radio"')
print(f"\n  Number of radio buttons: {radio_count}")
print(f"  Expected: 1 (for Cash on Delivery only)")

print("\n" + "=" * 80)
if not any(keyword in content for keyword, _ in keywords_to_check) and cod_check and radio_count == 1:
    print("🎉 SUCCESS: Checkout page shows ONLY Cash on Delivery!")
    print("   ✅ No UPI Payment option")
    print("   ✅ No Online Payment option")
    print("   ✅ No Razorpay references")
    print("   ✅ Cash on Delivery is available")
else:
    print("⚠️  WARNING: Checkout page may still have extra payment options!")
print("=" * 80)
