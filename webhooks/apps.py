# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class WebhooksConfig(AppConfig):
    name = 'webhooks'

    def ready(self):
        from webhooks.signals import webhook_pinged
