"""
# SETUP SETTINGS #
    **  fill all values

    **  copy this file in your settings
        OR
        rename and remove 'sample_' from this file
        add 'from core.resources.app_settings import *' in project settings.py
        add 'core/resources/app_settings.py' in .gitignore
"""
EE_INTEGRATION = {
    'CLEARBIT': {
        'key': '',
    },
    'SENDGRID': {
        'key': '',
    },
    'PUSHER_APP': {
        'ID': '',
        'key': '',
        'secret': ''
    }
}
SEND_EMAIL = None
TO_ADMIN_ONLY = None
EE_ADMIN_EMAIL = ''
