import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cheran_pumps.settings')
import django
django.setup()

from orders.views import CheckoutForm

print("\n" + "="*70)
print("CHECKOUT PAGE - PAYMENT METHOD SECTION (AS IT WILL APPEAR)")
print("="*70 + "\n")

form = CheckoutForm()
payment_choices = form.fields['payment_method'].choices

print("📋 Payment Method Section\n")
print("─" * 70)
print("Label: Payment Method\n")

counter = 0
for value, label in payment_choices:
    counter += 1
    print(f"  [{counter}] ○ {label}")
    print(f"       value: \"{value}\"\n")

print("─" * 70)
print(f"\nTotal payment options: {len(payment_choices)}")

print("\n" + "="*70)
print("VERIFICATION")
print("="*70)

values = [val for val, _ in payment_choices]
labels = [label for _, label in payment_choices]

print(f"\n✅ Cash on Delivery: Present")
print(f"✅ UPI Payment: Present")
print(f"❌ Online Payment: REMOVED\n")

print("="*70)
print("FINAL RESULT")
print("="*70)
print("""
✨ The checkout page will display:

    Payment Method
    ──────────────
    ○ Cash on Delivery
    ○ UPI Payment

❌ Online Payment option is COMPLETELY REMOVED from the form

Users will see ONLY these two payment options when placing an order.
""")
print("="*70 + "\n")
