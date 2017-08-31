# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        # App Imports
        from engine import redirect_noreply, activities_received

        # Package Imports
        import clearbit

        # Django Imports
        from django.conf import settings

        clearbit.key = settings.EE_INTEGRATION['CLEARBIT']['key']
