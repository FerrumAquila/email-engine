# App Imports
import models

# Django Imports
from django import forms
from django.contrib import admin


class CustomerSettingsCreationForm(forms.ModelForm):
    class Meta:
        model = models.CustomerSettings
        fields = ('customer_id', 'email_from_name')


class CustomerSettingsAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'email_from_name')
    form = CustomerSettingsCreationForm


admin.site.register(models.CustomerSettings, CustomerSettingsAdmin)
