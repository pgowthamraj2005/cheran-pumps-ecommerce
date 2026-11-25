import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cheran_pumps.settings')
import django
django.setup()

from django.db import connection
from django.db.migrations.loader import MigrationLoader
from orders.models import Order
from orders.views import CheckoutForm

print("\n" + "="*70)
print("PAYMENT METHOD CONFIGURATION VERIFICATION")
print("="*70)

print("\n1. DATABASE MIGRATIONS")
print("-" * 70)
loader = MigrationLoader(None, ignore_no_migrations=True)
orders_migrations = [key for key in loader.disk_migrations.keys() if key[0] == 'orders']
print(f"   Total migrations in orders app: {len(orders_migrations)}")
for migration_name in sorted(orders_migrations):
    app, name = migration_name
    print(f"   ✓ {name}")

print("\n2. MODEL PAYMENT CHOICES")
print("-" * 70)
print("   Order.PAYMENT_CHOICES:")
for value, label in Order.PAYMENT_CHOICES:
    print(f"      ☑ {value:10} = '{label}'")

print("\n3. CHECKOUT FORM PAYMENT METHOD")
print("-" * 70)
form = CheckoutForm()
payment_choices = form.fields['payment_method'].choices
print(f"   Total options: {len(payment_choices)}")
for value, label in payment_choices:
    print(f"      ☑ {value:10} = '{label}'")

print("\n4. VERIFICATION SUMMARY")
print("-" * 70)

# Create dictionaries for easy checking
model_choices_dict = dict(Order.PAYMENT_CHOICES)
form_choices_dict = dict(payment_choices)

checks = {
    "Model has 'cod' (Cash on Delivery)": 'cod' in model_choices_dict,
    "Model has 'upi' (UPI Payment)": 'upi' in model_choices_dict,
    "Model does NOT have 'online' (Online Payment)": 'online' not in model_choices_dict,
    "Form has 'cod' (Cash on Delivery)": 'cod' in form_choices_dict,
    "Form has 'upi' (UPI Payment)": 'upi' in form_choices_dict,
    "Form does NOT have 'online' (Online Payment)": 'online' not in form_choices_dict,
    "Model and Form choices match": model_choices_dict == form_choices_dict,
    "Total payment options = 2": len(model_choices_dict) == 2,
}

all_passed = True
for check_name, result in checks.items():
    status = "✅" if result else "❌"
    print(f"   {status} {check_name}")
    if not result:
        all_passed = False

print("\n" + "="*70)
if all_passed:
    print("🎉 SUCCESS: Checkout page will show ONLY:")
    print("   ○ Cash on Delivery")
    print("   ○ UPI Payment")
    print("\n   ❌ NO Online Payment option")
else:
    print("❌ ERROR: Configuration is not correct!")
print("="*70 + "\n")
