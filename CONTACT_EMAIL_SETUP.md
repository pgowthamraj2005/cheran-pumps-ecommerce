# Contact Page Email Setup Guide

This guide explains how to set up and configure the contact page with email functionality for the Cheran Pumps project.

## Overview

The contact page allows visitors to send messages which are:
1. Saved to the database (`Contact` model)
2. Sent to the visitor as a confirmation email
3. Sent to the admin as a notification email

## Features Implemented

✅ Contact form with validation
✅ Email sending to user (confirmation)
✅ Email sending to admin (notification)
✅ Admin panel to view and manage contact queries
✅ Mark queries as resolved
✅ Modal view for full message details
✅ Database tracking with timestamps

## Database Schema

```
Contact Model:
- name (CharField)
- email (EmailField)
- phone (CharField)
- subject (CharField)
- message (TextField)
- created_at (DateTimeField) - Auto-set on creation
- is_resolved (BooleanField) - Default: False
```

## Email Configuration

### For Development (Console Backend)

The default configuration sends emails to the console output:

```python
# In cheran_pumps/settings.py (already configured)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'cheran_pumps@example.com'
ADMIN_EMAIL = 'admin@cheran-pumps.local'
```

This is perfect for testing as no actual emails are sent.

### For Production (Gmail SMTP)

Update your environment variables and settings:

#### Step 1: Set up Gmail
1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Enable 2-Factor Authentication
3. Generate an App Password for your application
4. Copy the 16-character password

#### Step 2: Update Environment Variables

Create a `.env` file in the project root:

```bash
# .env
DJANGO_SECRET_KEY=your-secret-key-here
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-character-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
ADMIN_EMAIL=admin@cheran-pumps.local
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

#### Step 3: Update Settings
Uncomment the SMTP configuration in `cheran_pumps/settings.py`:

```python
# Email Configuration for Production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'your-email@gmail.com')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@cheran-pumps.local')
```

#### Step 4: Install python-decouple (optional, for .env support)

```bash
pip install python-decouple
```

Then in settings.py:
```python
from decouple import config

EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
```

## File Structure

```
cheran_pumps/
├── products/
│   ├── models.py              # Contact model
│   ├── forms.py               # ContactForm with styled widgets
│   ├── views.py               # contact() view with email logic
│   ├── admin.py               # Admin configuration for Contact
│   └── urls.py                # URL routing (already configured)
├── templates/
│   ├── products/
│   │   └── contact.html       # Public contact form template
│   └── admin_panel/
│       └── contact_list.html  # Admin contact management
├── cheran_pumps/
│   ├── settings.py            # Email configuration
│   └── urls.py
└── manage.py
```

## Usage

### For Users

1. Navigate to `/contact/` on the website
2. Fill in the contact form:
   - Name (required)
   - Email (required)
   - Phone (optional)
   - Subject (required)
   - Message (required)
3. Click "Send Message"
4. User receives a confirmation email
5. Admin receives a notification email

### For Admins

1. Go to `/admin/` → Products → Contacts
2. View all contact submissions
3. Click the "View" button to see full message details
4. Use "Reply via Email" to respond directly
5. Mark as "Resolved" when handled

## Email Templates

The system uses plain text emails for maximum compatibility. You can customize the email content in:

**File:** `products/views.py` → `contact()` function

### User Confirmation Email
Sent to the visitor with their reference details and confirmation of message receipt.

### Admin Notification Email
Sent to the admin with full contact details and the complete message.

## Troubleshooting

### Emails not sending?

1. **Check EMAIL_BACKEND:**
   ```python
   python manage.py shell
   >>> from django.conf import settings
   >>> print(settings.EMAIL_BACKEND)
   ```

2. **For Console Backend (Development):**
   - Check the terminal/console output where Django is running
   - Emails appear in the terminal, not sent to real addresses

3. **For Gmail SMTP:**
   - Verify 2FA is enabled
   - Generate a new App Password
   - Check EMAIL_HOST_USER and EMAIL_HOST_PASSWORD environment variables
   - Ensure "Less secure apps" is disabled (if not using App Passwords)

4. **Test email sending:**
   ```python
   python manage.py shell
   >>> from django.core.mail import send_mail
   >>> send_mail(
   ...     'Test Subject',
   ...     'Test Message',
   ...     'from@example.com',
   ...     ['to@example.com'],
   ... )
   1  # Returns 1 if successful
   ```

## Customization

### Modify Email Content

Edit the email templates in `products/views.py`:

```python
user_subject = "Custom subject here"
user_message = "Custom message here"

admin_subject = "Custom admin subject"
admin_message = "Custom admin message"
```

### Add More Fields

1. Update the `Contact` model in `products/models.py`
2. Run migrations:
   ```bash
   python manage.py makemigrations products
   python manage.py migrate
   ```
3. Update `ContactForm` in `products/forms.py`
4. Update templates as needed

### Change Email Recipients

Update `ADMIN_EMAIL` in settings.py or add multiple admin emails:

```python
# In products/views.py contact() function
admin_emails = ['admin1@example.com', 'admin2@example.com']
send_mail(
    admin_subject,
    admin_message,
    settings.DEFAULT_FROM_EMAIL,
    admin_emails,  # List of email addresses
    fail_silently=False,
)
```

## Security Notes

⚠️ **Important:**

1. Never commit `.env` file to version control
2. Add `.env` to `.gitignore`
3. Use environment variables for sensitive data
4. Never hardcode email credentials
5. Validate and sanitize user input (Django handles this)
6. Use HTTPS in production
7. Consider adding CAPTCHA for public forms

## API Reference

### Contact Model Methods

```python
from products.models import Contact

# Get all contacts
contacts = Contact.objects.all()

# Get unresolved contacts
pending = Contact.objects.filter(is_resolved=False)

# Get contacts by date range
from datetime import datetime, timedelta
recent = Contact.objects.filter(
    created_at__gte=datetime.now() - timedelta(days=7)
)

# Mark as resolved
contact = Contact.objects.get(id=1)
contact.is_resolved = True
contact.save()

# Search
results = Contact.objects.filter(
    Q(name__icontains='search') | 
    Q(email__icontains='search') |
    Q(message__icontains='search')
)
```

### URL Routes

| Route | Name | Purpose |
|-------|------|---------|
| `/contact/` | `contact` | Public contact form |
| `/admin/contacts/` | `admin_contact_list` | Admin view all queries |
| `/admin/contacts/<id>/resolve/` | `admin_contact_resolve` | Mark as resolved |

## Next Steps

1. Configure your preferred email backend
2. Test the contact form with test data
3. Verify emails are being sent
4. Customize email templates if needed
5. Monitor the admin panel for new messages
6. Respond to customer queries promptly

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Django email documentation
3. Consult the project README

---

**Last Updated:** July 15, 2024
**Project:** Cheran Pumps - Django E-Commerce
