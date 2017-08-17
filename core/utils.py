# App Imports
import models
import serialisers

# Package Imports
import clearbit
import sendgrid
from annoying.functions import get_object_or_None
from sendgrid.helpers.mail import Mail, Email, Content, CustomArg

# Django Imports
from django.conf import settings
from django.core.urlresolvers import reverse


class EmailHandler(object):
    @classmethod
    def fetch_lite(cls, email_id):
        return clearbit.Person.find(email=email_id)

    @classmethod
    def send_email(cls, customer_id, _from_email, _to_email, subject, content, extra_args=None):

        customer_settings = get_object_or_None(models.CustomerSettings, customer_id=customer_id)

        if customer_settings:
            _from_email = customer_settings.email_from_email or _from_email
            _from_name = customer_settings.email_from_name or 'Vetted'
        else:
            _from_email = _from_email
            _from_name = 'Vetted'
        from_email = Email(_from_email, _from_name)

        if settings.TO_ADMIN_ONLY and 'aetos-force' not in _to_email:
            _to_email = settings.EE_ADMIN_EMAIL
        else:
            _to_email = _to_email
        to_email = Email(_to_email)

        content = Content("text/html", content)
        mail = Mail(from_email, subject, to_email, content)
        if extra_args:
            processed_extra_args = [CustomArg(**extra_arg) for extra_arg in extra_args]
            for processed_extra_arg in processed_extra_args:
                mail.add_custom_arg(processed_extra_arg)
            email_params = '--'.join([args['key'] + '-' + args['value'] for args in extra_args])
            email_domain = '@parse.thevetted.com'
            mail.reply_to = Email(email_params + email_domain, 'No Reply')

        if settings.SEND_EMAIL:
            sg = sendgrid.SendGridAPIClient(apikey=settings.EE_INTEGRATION['SENDGRID']['key'])
            return sg.client.mail.send.post(request_body=mail.get())


class EmailActivitiesHandler(object):
    @classmethod
    def get_latest_status(cls, email_object_id):
        activity = cls.get_latest_status_activity(email_object_id)
        return StatusHandler.get_activity_object(activity) if activity else {'status': 'sent'}

    @classmethod
    def get_latest_status_activity(cls, email_object_id):
        activities = models.ActivityEvent.objects.filter(sg_message_id__icontains=email_object_id)
        return StatusHandler(activities).get_main_step() if activities else None

    @classmethod
    def group_by_tenant_id(cls, mixed_request_datas):
        grouped_request_datas = dict()
        for request_data in mixed_request_datas:
            tenant_id = request_data.get('tenant_id') or 'legacy-emails'
            if tenant_id not in grouped_request_datas:
                grouped_request_datas.update({tenant_id: [request_data]})
            else:
                grouped_request_datas[tenant_id].append(request_data)
        return grouped_request_datas


class StatusHandler(object):
    STATUSES = {
        'processed': {'status': 'processed', 'priority': 1},
        'dropped': {'status': 'failed', 'priority': 2},
        'delivered': {'status': 'delivered', 'priority': 3},
        'deferred': {'status': 'failed', 'priority': 4},
        'bounce': {'status': 'failed', 'priority': 5},
        'open': {'status': 'opened', 'priority': 6},
        'click': {'status': 'clicked', 'priority': 7},
        'spamreport': {'status': 'spamreport', 'priority': 0},
        'unsubscribe': {'status': 'unsubscribe', 'priority': 0},
        'group_unsubscribe': {'status': 'unsubscribe', 'priority': 0},
        'group_resubscribe': {'status': 'resubscribe', 'priority': 0},
    }

    def __init__(self, activities):
        self.activities = activities
        self._main_step_activity = None

    @classmethod
    def get_activity_object(cls, activity):
        return cls.STATUSES[activity.name]

    @classmethod
    def _get_activity_status(cls, activity):
        return cls.get_activity_object(activity)['status']

    @classmethod
    def _get_activity_priority(cls, activity):
        return cls.get_activity_object(activity)['priority']

    def _process_step(self, activity):
        if not self._main_step_activity:
            self._main_step_activity = activity
        else:
            activity_priority = self._get_activity_priority(activity)
            main_step_priority = self._get_activity_priority(self._main_step_activity)
            if activity_priority and activity_priority >= main_step_priority:
                self._main_step_activity = activity

    def get_main_step(self):
        for activity in self.activities:
            self._process_step(activity)
        return self._main_step_activity


class IncomingMailHandler(object):
    @classmethod
    def get_data_json(cls, incoming_mail):
        return serialisers.ParseIncomingMail(incoming_mail).required_json

    @classmethod
    def email_from_text(cls, incoming_mail):
        return 'Email From: %s' % (incoming_mail.mail_from or 'Unknown')

    @classmethod
    def open_email_button(cls, incoming_mail):
        return '<span class="open_email_btn" data-email_data="%s">Open email</span>' % reverse(
            'email_engine:incoming_mail_data', kwargs={'pk': incoming_mail.pk})

    @classmethod
    def reply_email_help_text(cls, incoming_mail):
        return 'Mention @%s to reply' % incoming_mail.mail_from.split('@')[0]

    @classmethod
    def get_params_from_email(cls, incoming_mail):
        params = dict()
        for param_string in incoming_mail.mail_to.split('@')[0].split('--'):
            key = param_string.split('-')[0]
            value = param_string.split('-')[1]
            params.update({key: value})
        return params
