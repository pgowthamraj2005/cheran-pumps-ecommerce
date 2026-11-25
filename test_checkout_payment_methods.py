7#!/usr/bin/env python
"""Test script to verify checkout payment methods."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cheran_pumps.settings')
django.setup()

from orders.models import Order
from orders.views import CheckoutForm

# Check model choices
print("=" * 70)
print("PAYMENT_CHOICES in Order model:")
print("=" * 70)
for choice_value, choice_label in Order.PAYMENT_CHOICES:
    print(f"  [{choice_value}] {choice_label}")

print("\n" + "=" * 70)
print("Payment method choices in CheckoutForm:")
print("=" * 70)
form = CheckoutForm()
for choice_value, choice_label in form.fields['payment_method'].choices:
    print(f"  [{choice_value}] {choice_label}")

print("\n" + "=" * 70)
print("Form widget HTML rendering (first 500 chars):")
print("=" * 70)
form = CheckoutForm()
rendered = str(form['payment_method'])
print(rendered[:500])

print("\n" + "=" * 70)
print("VERIFICATION RESULTS:")
print("=" * 70)

has_cod = any('cod' in str(choice[0]).lower() for choice in form.fields['payment_method'].choices)
has_upi = any('upi' in str(choice[0]).lower() for choice in form.fields['payment_method'].choices)
has_online = any('online' in str(choice[0]).lower() for choice in form.fields['payment_method'].choices)

print(f"✅ Has Cash on Delivery (COD): {has_cod}")
print(f"{'❌' if has_upi else '✅'} Has UPI Payment: {has_upi}")
print(f"{'❌' if has_online else '✅'} Has Online Payment: {has_online}")

if has_cod and not has_upi and not has_online:
    print("\n🎉 SUCCESS: Only Cash on Delivery is available!")
else:
    print("\n⚠️ ERROR: Payment methods configuration is incorrect!")
    
print("\n" + "=" * 70)
