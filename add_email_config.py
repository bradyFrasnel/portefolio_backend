import re

with open('config/settings.py', 'r', encoding='utf-8') as f:
    content = f.read()

email_config = '''
# Configuration Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='mokumabrady13@gmail.com')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
'''

if 'EMAIL_BACKEND' not in content:
    content += '\n' + email_config

with open('config/settings.py', 'w', encoding='utf-8') as f:
    f.write(content)
