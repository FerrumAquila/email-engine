# Django Imports
from django.dispatch import Signal


webhook_pinged = Signal(providing_args=['request_data'])