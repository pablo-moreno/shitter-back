from django.conf import settings

"""
Defines the maximum of sign up requests allowed for a single IP
"""
AUTH_SIGN_UP_BY_IP_LIMIT = getattr(settings, 'AUTH_SIGN_UP_BY_IP_LIMIT', 10)

"""
Defines maximum login retries
"""
MAX_LOGIN_RETRIES = getattr(settings, 'MAX_LOGIN_RETRIES', 10)

"""
Defines if the user must be set to inactive after maximum login retries failed.
"""
SET_USER_INACTIVE_AFTER_MAX_LOGIN_RETRIES = getattr(settings, 'SET_USER_INACTIVE_AFTER_MAX_LOGIN_RETRIES', False)

"""
Defines the password reset email text
"""
EMAIL_RESET_PASSWORD_TEMPLATE_NAME = getattr(
    settings,
    'EMAIL_RESET_PASSWORD_TEMPLATE_NAME',
    'authentication/password_reset_email.txt'
)

"""
Defines the password reset email template to use
"""
HTML_EMAIL_RESET_PASSWORD_TEMPLATE_NAME = getattr(
    settings,
    'HTML_EMAIL_RESET_PASSWORD_TEMPLATE_NAME',
    'authentication/password_reset_email.html'
)

"""
Defines the reset password email subject template
"""
SUBJECT_EMAIL_RESET_PASSWORD_NAME = getattr(
    settings,
    'SUBJECT_EMAIL_RESET_PASSWORD_NAME',
    'authentication/password_reset_subject.txt'
)
