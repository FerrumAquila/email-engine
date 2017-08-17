# App Imports
import views

# Django Imports
from django.conf.urls import url


# namespace
urlpatterns = [
    'lifecycles.views',

    # POST: WEBHOOKS #
    url(r'^email-activities/$', views.email_activities_webhook, name='email_activities'),
    url(r'^incoming-mail/$', views.incoming_mail_webhook, name='incoming_mail'),
]

