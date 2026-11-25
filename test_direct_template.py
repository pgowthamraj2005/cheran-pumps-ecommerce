#!/usr/bin/env python
"""Direct template render test to verify checkout page."""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cheran_pumps.settings')
django.setup()

from django.template import Context, Template
from django.template.loader import render_to_string
from orders.views import CheckoutForm
from products.models import Product
from django.contrib.auth import get_user_model

# Create a mock user and request context
User_model = get_user_model()
user = User_model.objects.filter(username='testuser').first()
if not user:
    user = User_model.objects.create_user('testuser', 'test@test.com', 'testpass123')

# Get some products for the cart
products = Product.objects.all()[:2]

# Create mock items for the order summary
items = []
for product in products:
    items.append({
        'product': product,
        'quantity': 1,
        'subtotal': product.price
    })

total = sum(item['subtotal'] for item in items)

# Create the form
form = CheckoutForm()

# Render the template
print("=" * 80)
print("CHECKOUT TEMPLATE RENDER TEST")
print("=" * 80)

try:
    # Read the template file directly
    with open('templates/orders/checkout.html', 'r') as f:
        template_content = f.read()
    
    print("\nTemplate content (first 500 chars):")
    print("-" * 80)
    print(template_content[:500])
    print("...")
    print("-" * 80)
    
    # Check for problematic keywords in the template source
    print("\n" + "=" * 80)
    print("TEMPLATE SOURCE ANALYSIS:")
    print("=" * 80)
    
    keywords = {
        'upi': 'UPI Payment',
        'razorpay': 'Razorpay',
        'online': 'Online Payment',
        '{% url "create_razorpay_order"': 'Razorpay URL',
        '{% url "verify_payment"': 'Payment verification URL',
        'checkout.razorpay': 'Razorpay script',
        'upi-payment-note': 'UPI note element',
    }
    
    has_bad_keywords = False
    for keyword, description in keywords.items():
        if keyword in template_content.lower():
            print(f"  ❌ FOUND: {description} ('{keyword}')")
            has_bad_keywords = True
        else:
            print(f"  ✅ NOT FOUND: {description}")
    
    # Check for good keywords
    print(f"\n  {'✅' if 'Cash on Delivery' in template_content else '❌'} 'Cash on Delivery' present")
    print(f"  {'✅' if 'checkout-form' in template_content else '❌'} Checkout form present")
    print(f"  {'✅' if 'payment_method' in template_content else '❌'} Payment method field present")
    
    print("\n" + "=" * 80)
    if not has_bad_keywords:
        print("🎉 SUCCESS: Template is clean!")
        print("   ✅ No UPI references")
        print("   ✅ No Razorpay references")
        print("   ✅ No Online Payment references")
        print("   ✅ Template ready for rendering")
    else:
        print("❌ ERROR: Template still contains unwanted code!")
    print("=" * 80)
    
except Exception as e:
    print(f"Error reading template: {e}")

# Also test the form rendering directly
print("\n" + "=" * 80)
print("PAYMENT METHOD FORM RENDERING:")
print("=" * 80)

form = CheckoutForm()
form_html = str(form['payment_method'])

print("\nForm HTML (payment_method field):")
print("-" * 80)
print(form_html)
print("-" * 80)

radio_count = form_html.count('type="radio"')
has_cod_value = 'value="cod"' in form_html
has_upi_value = 'value="upi"' in form_html

print(f"\n  Radio button count: {radio_count}")
print(f"  COD value present: {has_cod_value}")
print(f"  UPI value present: {has_upi_value}")

if radio_count == 1 and has_cod_value and not has_upi_value:
    print("\n✅ Form renders correctly with ONLY Cash on Delivery!")
else:
    print("\n❌ Form has issues!")
