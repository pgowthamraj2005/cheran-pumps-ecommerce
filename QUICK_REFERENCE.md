#!/bin/bash
# Quick Reference Commands for Cheran Pumps Contact Form

# ═════════════════════════════════════════════════════════════
# USEFUL COMMANDS
# ═════════════════════════════════════════════════════════════

# Run Development Server
# python manage.py runserver

# Open Django Shell for Testing
# python manage.py shell

# ═════════════════════════════════════════════════════════════
# DATABASE COMMANDS
# ═════════════════════════════════════════════════════════════

# Create Migrations
# python manage.py makemigrations products

# Apply Migrations
# python manage.py migrate

# View All Contacts (Django Shell)
# >>> from products.models import Contact
# >>> Contact.objects.all()

# View Pending Contacts Only
# >>> Contact.objects.filter(is_resolved=False)

# Mark Contact as Resolved
# >>> contact = Contact.objects.get(id=1)
# >>> contact.is_resolved = True
# >>> contact.save()

# Delete Test Contacts
# >>> Contact.objects.all().delete()

# ═════════════════════════════════════════════════════════════
# EMAIL TESTING COMMANDS
# ═════════════════════════════════════════════════════════════

# Test Email Configuration (Django Shell)
# >>> from django.conf import settings
# >>> print(settings.EMAIL_BACKEND)
# >>> print(settings.DEFAULT_FROM_EMAIL)

# Send Test Email
# >>> from django.core.mail import send_mail
# >>> send_mail(
# ...     'Test Subject',
# ...     'Test Message',
# ...     'from@example.com',
# ...     ['to@example.com'],
# ... )

# ═════════════════════════════════════════════════════════════
# ADMIN PANEL URLS
# ═════════════════════════════════════════════════════════════

# Django Admin
# http://localhost:8000/admin/

# Contact Management
# http://localhost:8000/admin/products/contact/

# Products Admin
# http://localhost:8000/admin/products/

# ═════════════════════════════════════════════════════════════
# WEBSITE URLS
# ═════════════════════════════════════════════════════════════

# Contact Page
# http://localhost:8000/contact/

# Home Page
# http://localhost:8000/

# Products List
# http://localhost:8000/products/

# ═════════════════════════════════════════════════════════════
# FILE LOCATIONS
# ═════════════════════════════════════════════════════════════

# Contact Model
# products/models.py

# Contact Form
# products/forms.py

# Contact View
# products/views.py

# Contact Admin
# products/admin.py

# Public Template
# templates/products/contact.html

# Admin Template
# templates/admin_panel/contact_list.html

# Email Settings
# cheran_pumps/settings.py

# URLs
# products/urls.py
# admin_panel/urls.py

# ═════════════════════════════════════════════════════════════
# DOCUMENTATION FILES
# ═════════════════════════════════════════════════════════════

# Complete Setup Guide
# CONTACT_EMAIL_SETUP.md

# Implementation Overview
# IMPLEMENTATION_SUMMARY.md

# Verification Checklist
# VERIFICATION_CHECKLIST.md

# This Quick Reference
# QUICK_REFERENCE.md

# ═════════════════════════════════════════════════════════════
# ENVIRONMENT VARIABLES (.env)
# ═════════════════════════════════════════════════════════════

# For Development (Console Backend - Default)
# No additional setup needed!

# For Production (Gmail SMTP)
# EMAIL_HOST_USER=your-email@gmail.com
# EMAIL_HOST_PASSWORD=your-app-password
# DEFAULT_FROM_EMAIL=your-email@gmail.com
# ADMIN_EMAIL=admin@cheran-pumps.local

# ═════════════════════════════════════════════════════════════
# TROUBLESHOOTING QUICK LINKS
# ═════════════════════════════════════════════════════════════

# Emails not appearing?
# 1. Check EMAIL_BACKEND in settings.py
# 2. For development, check terminal output
# 3. For production, verify SMTP credentials
# See: CONTACT_EMAIL_SETUP.md → Troubleshooting

# Form not working?
# 1. Check browser console for JavaScript errors
# 2. Verify all required fields are filled
# 3. Check server error logs
# Run: python manage.py runserver

# Admin not showing contacts?
# 1. Login as staff user
# 2. Navigate to /admin/products/contact/
# 3. Check database: >>> Contact.objects.all()

# ═════════════════════════════════════════════════════════════
# KEY FEATURES SUMMARY
# ═════════════════════════════════════════════════════════════

# ✓ Public Contact Form
#   - Name, Email, Phone, Subject, Message
#   - Bootstrap 5 styling
#   - Form validation
#   - Error handling

# ✓ Email Notifications
#   - Confirmation email to user
#   - Notification email to admin
#   - Console output in development

# ✓ Admin Management
#   - View all submissions
#   - Filter by status
#   - Mark as resolved
#   - Direct email reply
#   - Full message details

# ✓ Database
#   - Persistent storage
#   - Status tracking
#   - Timestamps
#   - Search capability

# ═════════════════════════════════════════════════════════════
# DEPLOYMENT CHECKLIST
# ═════════════════════════════════════════════════════════════

# [ ] Configure .env with production email settings
# [ ] Test email sending in production environment
# [ ] Set DEBUG=False in settings.py
# [ ] Configure ALLOWED_HOSTS
# [ ] Set up SMTP credentials securely
# [ ] Run migrations on production database
# [ ] Test contact form on live site
# [ ] Verify admin panel access
# [ ] Set up monitoring for new contacts
# [ ] Configure email notifications for team

# ═════════════════════════════════════════════════════════════

# Last Updated: July 15, 2024
# Project: Cheran Pumps - Django E-Commerce
