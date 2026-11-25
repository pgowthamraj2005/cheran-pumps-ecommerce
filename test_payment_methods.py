import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cheran_pumps.settings')
import django
django.setup()

from orders.models import Order
from orders.views import CheckoutForm

print('Payment Choices in Order model:')
for choice in Order.PAYMENT_CHOICES:
    print('  ' + choice[0] + ': ' + choice[1])

print('\nPayment Method choices in CheckoutForm:')
form = CheckoutForm()
for choice in form.fields['payment_method'].choices:
    print('  ' + choice[0] + ': ' + choice[1])

cod_available = 'cod' in dict(Order.PAYMENT_CHOICES)
upi_available = 'upi' in dict(Order.PAYMENT_CHOICES)
online_available = 'online' in dict(Order.PAYMENT_CHOICES)

print('\nVerification:')
print('Has Cash on Delivery: ' + str(cod_available))
print('Has UPI Payment: ' + str(upi_available))
print('Has Online Payment: ' + str(online_available))

if cod_available and upi_available and not online_available:
    print('\nSUCCESS: Only COD and UPI are available!')
else:
    print('\nERROR: Payment methods are not configured correctly')
