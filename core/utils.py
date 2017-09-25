# App Imports
import models
import contracts

# Package Imports
import clearbit
import sendgrid
from annoying.functions import get_object_or_None
from sendgrid.helpers.mail import Mail, Email, Content, CustomArg

# Django Imports
from django.conf import settings
from django.core.urlresolvers import reverse


class PrepEmail(object):
    def __init__(self, customer_id, _from_email, _to_email, subject, content,
                 email_args=None, custom_args=None, async=True):
        self.customer_settings = get_object_or_None(models.CustomerSettings, customer_id=customer_id)
        self._from_email = _from_email
        self._to_email = _to_email
        self.subject = subject
        self.content = content
        self._email_args = email_args
        self._custom_args = custom_args
        self.async = async
        self._mail_object = None

    @property
    def mail(self):
        content = Content("text/html", self.content)
        self._mail_object = Mail(self.from_email, self.subject, self.to_email, content)
        self._set_custom_args()
        self._set_email_args()
        return self._mail_object

    @property
    def from_email(self):
        if self.customer_settings:
            _from_email = self.customer_settings.email_from_email or self._from_email
            _from_name = self.customer_settings.email_from_name or 'Vetted'
        else:
            _from_email = self._from_email
            _from_name = 'Vetted'
        return Email(_from_email, _from_name)

    @property
    def to_email(self):
        if settings.TO_ADMIN_ONLY and 'aetos-force' not in self._to_email:
            _to_email = settings.EE_ADMIN_EMAIL
        else:
            _to_email = self._to_email
        return Email(_to_email)

    def _set_custom_args(self):
        if self._custom_args:
            processed_custom_args = [CustomArg(**extra_arg) for extra_arg in self._custom_args]
            for processed_extra_arg in processed_custom_args:
                self._mail_object.add_custom_arg(processed_extra_arg)

    def _set_email_args(self):
        if self._email_args:
            email_params = '--'.join([key + '-' + value for key, value in self._email_args.items()])
            email_domain = '@parse.thevetted.com'
            if settings.DEBUG:
                email_domain = '@parse.thevetted.net'
            self._mail_object.reply_to = Email(email_params + email_domain, 'No Reply')


class EmailHandler(object):
    @classmethod
    def fetch_lite(cls, email_id):
        return clearbit.Person.find(email=email_id)

    @classmethod
    def send_email(cls, customer_id, _from_email, _to_email, subject, content,
                   email_args=None, custom_args=None, async=True):

        mail = PrepEmail(customer_id, _from_email, _to_email, subject, content, email_args, custom_args).mail

        if settings.SEND_EMAIL:
            sg = sendgrid.SendGridAPIClient(apikey=settings.EE_INTEGRATION['SENDGRID']['key'])
            if async:
                return 'email sent', sg.client.mail.send.post(request_body=mail.get())
            return 'email processed', sg.client.mail.send.post(request_body=mail.get())


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
        return contracts.ParseIncomingMail(incoming_mail).required_json

    @classmethod
    def email_from_text(cls, incoming_mail):
        return 'Email From: %s' % (incoming_mail.mail_from or 'Unknown')

    @classmethod
    def open_email_button(cls, incoming_mail):
        return '<span class="open_email_btn" data-email_data="%s">Open email</span>' % reverse(
            'core:incoming_mail_data', kwargs={'pk': incoming_mail.pk})

    @classmethod
    def reply_email_help_text(cls, incoming_mail):
        return 'Mention @%s to reply' % incoming_mail.mail_from.split('@')[0]

    @classmethod
    def get_params_from_email(cls, incoming_mail):
        params = dict()
        reply_to_email = ''
        for email in incoming_mail.mail_to:
            if '@parse.thevetted' in email:
                reply_to_email = email
        if not reply_to_email:
            return dict()
        for param_string in reply_to_email.split('@')[0].split('--'):
            key = param_string.split('-')[0]
            value = param_string.split('-')[1]
            params.update({key: value})
        return params
