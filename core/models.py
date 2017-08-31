# App Imports
import webhooks
import serialisers
from core.resources import models


class SGMessageIdLink(models.AetosModel):
    object_id = models.CharField(max_length=127)
    object_type = models.CharField(max_length=127)
    sg_message_id = models.CharField(max_length=127)

    class Options:
        create_serialiser = serialisers.CreateSGMessageIdLink


class ActivityEvent(models.AetosModel):
    name = models.CharField(max_length=127)
    smtp_id = models.CharField(max_length=127)
    sg_event_id = models.CharField(max_length=127)
    sg_message_id = models.CharField(max_length=127)
    timestamp = models.DateTimeField()

    email = models.CharField(max_length=127, default='', blank=True, null=True)
    category = models.CharField(max_length=127, default='', blank=True, null=True)

    class Options:
        create_serialiser = webhooks.serialisers.CreateActivityEvent


class IncomingMail(models.AetosModel):
    mail_from = models.CharField(max_length=127)
    mail_to = models.CharField(max_length=127)
    mail_cc = models.CharField(max_length=127)
    subject = models.CharField(max_length=127)
    attachments = models.TextField(default='{}')
    info = models.TextField(default='{}')

    text = models.TextField(null=True)
    html = models.TextField(null=True)

    class Options:
        create_serialiser = webhooks.serialisers.CreateIncomingMail


class CustomerSettings(models.AetosModel):
    customer_id = models.PositiveIntegerField()
    email_from_name = models.CharField(max_length=63, default='No Reply')
