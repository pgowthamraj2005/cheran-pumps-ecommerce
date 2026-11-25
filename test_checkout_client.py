#!/usr/bin/env python
"""Test to verify the actual checkout page HTML output using Django test client."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cheran_pumps.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

# Get or create test user
User_model = get_user_model()
user = User_model.objects.filter(username='testuser').first()
if not user:
    user = User_model.objects.create_user('testuser', 'test@test.com', 'testpass123')
    print(f"✓ Created test user: {user.username}\n")

# Create a test client
client = Client()

# Login
logged_in = client.login(username='testuser', password='testpass123')
print(f"{'✓' if logged_in else '✗'} Login status: {logged_in}\n")

# Add an item to cart first
session = client.session
session['cart'] = {'1': 1}  # Add product with ID 1, quantity 1
session.save()

# Get the checkout page
print("=" * 80)
print("CHECKOUT PAGE HTML OUTPUT")
print("=" * 80)

response = client.get('/orders/checkout/')
content = response.content.decode('utf-8')

# Extract just the payment method section
import re
payment_section = re.search(r'<label class="form-label fw-bold">Payment Method.*?</div>\s*</div>\s*</div>', content, re.DOTALL)
if payment_section:
    print("\nPAYMENT METHOD SECTION:")
    print("-" * 80)
    payment_html = payment_section.group(0)
    # Clean up formatting
    payment_html = re.sub(r'\s+', ' ', payment_html)
    print(payment_html)
    print("-" * 80)

# Check for keywords
print("\n" + "=" * 80)
print("VERIFICATION RESULTS:")
print("=" * 80)

keywords_to_check = [
    ('upi', 'UPI Payment'),
    ('UPI', 'UPI uppercase'),
    ('razorpay', 'Razorpay'),
    ('Razorpay', 'Razorpay uppercase'),
    ('online', 'Online Payment'),
    ('Online', 'Online uppercase'),
    ('checkout.razorpay', 'Razorpay script'),
]

has_unwanted = False
for keyword, description in keywords_to_check:
    found = keyword in content.lower()
    status = "❌ FOUND" if found else "✅"
    if found:
        has_unwanted = True
    print(f"  {status} '{keyword}' ({description})")

# Check for Cash on Delivery
cod_check = 'Cash on Delivery' in content
print(f"\n  {'✅' if cod_check else '❌'} 'Cash on Delivery' found")

# Check for radio buttons
radio_count = content.count('type="radio"')
print(f"  {'✅' if radio_count == 1 else '❌'} Number of radio buttons: {radio_count} (expected: 1)")

# Check for form action
print(f"  {'✅' if 'checkout-form' in content else '❌'} Checkout form exists")

print("\n" + "=" * 80)
if not has_unwanted and cod_check and radio_count == 1:
    print("🎉 SUCCESS: Checkout page displays ONLY Cash on Delivery!")
    print("\n   ✅ No UPI Payment option visible")
    print("   ✅ No Online Payment option visible")
    print("   ✅ No Razorpay references")
    print("   ✅ Only 1 payment method available (COD)")
    print("   ✅ Cash on Delivery is clearly labeled")
else:
    print("⚠️  ERROR: Checkout page may still have extra payment options!")
    print(f"\n   Unwanted keywords found: {has_unwanted}")
    print(f"   COD available: {cod_check}")
    print(f"   Radio button count correct: {radio_count == 1}")
print("=" * 80)
