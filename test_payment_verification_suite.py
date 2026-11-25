# File: test_payment_verification_suite.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cheran_pumps.settings')
django.setup()

from django.test import Client
from accounts.models import User
from products.models import Product, Category
from orders.models import Order
from django.conf import settings
import hmac
import hashlib

def test_full_payment_suite():
    print("=" * 60)
    print("RUNNING COMPREHENSIVE PAYMENT & VERIFICATION TESTS")
    print("=" * 60)

    # 1. Setup user and product
    user, _ = User.objects.get_or_create(username='verify_user', defaults={'email': 'vuser@test.com'})
    user.set_password('pass123')
    user.save()

    cat, _ = Category.objects.get_or_create(name='Submersible Pumps', defaults={'slug': 'submersible-pumps'})
    product, _ = Product.objects.get_or_create(
        name='Premium Monobloc',
        defaults={'category': cat, 'price': 5499, 'stock': 15, 'is_active': True}
    )

    client = Client()
    client.login(username='verify_user', password='pass123')

    session = client.session
    session['cart'] = {str(product.id): 1}
    session.save()

    # 2. Test Dynamic QR code endpoint
    qr_res = client.get('/orders/gpay-qr/')
    assert qr_res.status_code == 200
    assert qr_res['Content-Type'] == 'image/png'
    print("[PASS] 1. Dynamic UPI QR endpoint generates live QR PNG")

    # 3. Test Razorpay Order Creation Endpoint
    rp_res = client.post('/orders/create_razorpay_order/')
    assert rp_res.status_code == 200
    rp_data = rp_res.json()
    assert 'razorpay_order_id' in rp_data or 'key_id' in rp_data
    assert rp_data.get('amount') == 549900  # 5499 * 100 paise
    print(f"[PASS] 2. Razorpay Order Creation generated amount: {rp_data.get('amount')} paise")

    # 4. Test Cryptographic Signature Verification Logic
    key_secret = settings.RAZORPAY_KEY_SECRET or 'test_secret'
    dummy_order_id = 'order_test_12345'
    dummy_payment_id = 'pay_test_67890'
    msg = f"{dummy_order_id}|{dummy_payment_id}".encode('utf-8')
    valid_sig = hmac.new(key_secret.encode('utf-8'), msg, hashlib.sha256).hexdigest()

    # Fake invalid signature test
    invalid_verify_res = client.post('/orders/verify_payment/', {
        'razorpay_order_id': dummy_order_id,
        'razorpay_payment_id': dummy_payment_id,
        'razorpay_signature': 'invalid_signature_hex',
        'address': 'Test Address',
        'payment_method': 'upi'
    })
    assert invalid_verify_res.status_code == 400
    print("[PASS] 3. Backend rejects invalid payment signature")

    # Valid signature test
    valid_verify_res = client.post('/orders/verify_payment/', {
        'razorpay_order_id': dummy_order_id,
        'razorpay_payment_id': dummy_payment_id,
        'razorpay_signature': valid_sig,
        'address': '456 Verified St, Coimbatore',
        'payment_method': 'upi'
    })
    assert valid_verify_res.status_code == 200
    res_json = valid_verify_res.json()
    assert res_json.get('success') is True

    verified_order = Order.objects.get(pk=res_json['order_id'])
    assert verified_order.payment_status == 'paid'
    assert verified_order.status == 'confirmed'
    assert verified_order.total_amount == 5499
    print(f"[PASS] 4. Backend verifies valid signature: Order #{verified_order.id} marked PAID and CONFIRMED")

    # 5. COD Order Flow test
    session = client.session
    session['cart'] = {str(product.id): 1}
    session.save()

    cod_res = client.post('/orders/checkout/', {
        'address': '789 COD St',
        'payment_method': 'cod',
    }, follow=True)
    assert cod_res.status_code == 200
    cod_order = Order.objects.filter(user=user, payment_method='cod').latest('created_at')
    assert cod_order.status == 'confirmed'
    print(f"[PASS] 5. COD flow remains intact: Order #{cod_order.id} CONFIRMED")

    print("\n" + "=" * 60)
    print("ALL VERIFICATION AND GATEWAY TESTS PASSED!")
    print("=" * 60)

if __name__ == '__main__':
    test_full_payment_suite()
