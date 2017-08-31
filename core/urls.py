# App Imports
import views

# Django Imports
from django.conf.urls import url


urlpatterns = [
    # GET
    url(r'^data/incoming-mail/pk/(?P<pk>\d+)/$', views.incoming_mail_data, name='incoming_mail_data'),
    url(r'^status/email-activities/pk/(?P<people_id>.*)/$', views.email_latest_status, name='email_latest_status'),
    url(r'^email-info/(?P<email_id>[a-z A-Z 0-9 \/ . @]+)/$', views.email_info, name='email_info'),

    # POST
    url(r'^send-mail/$', views.send_email, name='send_email'),
]
