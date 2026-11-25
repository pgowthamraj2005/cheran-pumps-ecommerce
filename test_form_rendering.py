import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cheran_pumps.settings')
import django
django.setup()

from orders.views import CheckoutForm

print("="*60)
print("CHECKOUT FORM PAYMENT METHOD OPTIONS")
print("="*60)

form = CheckoutForm()
payment_field = form.fields['payment_method']

print("\nPayment Method Radio Options:")
print("-" * 60)

# Render the form widget
widget_html = payment_field.widget.render('payment_method', None)
lines = widget_html.split('\n')
for line in lines:
    if line.strip():
        print(line)

print("\n" + "="*60)
print("ANALYSIS")
print("="*60)

print("\nOptions available in form:")
for value, label in payment_field.choices:
    print(f"  ☑ {value}: {label}")

print("\nVerification:")
options_values = [val for val, _ in payment_field.choices]
print(f"  ✅ Has Cash on Delivery (cod): {'cod' in options_values}")
print(f"  ✅ Has UPI Payment (upi): {'upi' in options_values}")
print(f"  ✅ NO Online Payment (online): {'online' not in options_values}")

if len(payment_field.choices) == 2 and 'cod' in options_values and 'upi' in options_values:
    print("\n✅ SUCCESS: Form renders ONLY Cash on Delivery and UPI Payment!")
else:
    print("\n❌ ERROR: Form does not have correct options!")

print("\n" + "="*60)
