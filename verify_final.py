import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cheran_pumps.settings')
import django
django.setup()

from orders.views import CheckoutForm
from orders.models import Order

print("\n" + "="*70)
print("FINAL PAYMENT METHOD VERIFICATION")
print("="*70 + "\n")

# Check model
print("1. Model PAYMENT_CHOICES:")
print("-" * 70)
for value, label in Order.PAYMENT_CHOICES:
    print(f"   ☑ {value:15} -> {label}")

print("\n2. CheckoutForm Payment Method Field:")
print("-" * 70)
form = CheckoutForm()
payment_field = form.fields['payment_method']
for value, label in payment_field.choices:
    print(f"   ☑ {value:15} -> {label}")

print("\n3. Rendered Form HTML:")
print("-" * 70)
html = payment_field.widget.render('payment_method', None)
for line in html.split('\n'):
    if line.strip():
        print(f"   {line.strip()}")

print("\n4. VERIFICATION:")
print("-" * 70)
choices_dict = dict(payment_field.choices)
has_cod = 'cod' in choices_dict
has_upi = 'upi' in choices_dict
has_online = 'online' in choices_dict

print(f"   ✅ Has 'cod' (Cash on Delivery): {has_cod}")
print(f"   ✅ Has 'upi' (UPI Payment): {has_upi}")
print(f"   ✅ NO 'online' (Online Payment): {not has_online}")

if has_cod and has_upi and not has_online:
    print("\n" + "="*70)
    print("✅ SUCCESS!")
    print("="*70)
    print("\nCheckout page will display:")
    print("  ○ Cash on Delivery")
    print("  ○ UPI Payment")
    print("\n❌ REMOVED: Online Payment")
    print("="*70 + "\n")
else:
    print("\n❌ ERROR: Payment methods not configured correctly!\n")
