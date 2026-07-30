from .base import *

DEBUG = False

# Production specific settings can be added here
# Ensure that CSRF_COOKIE_SECURE and SESSION_COOKIE_SECURE are True in production
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
