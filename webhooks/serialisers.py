# Package Imports
from core.resources.serialisers import *


class CreateIncomingMail(Serializer):
    BODY_MAP = {
        'mail_from': ('envelope__from', as_is),
        'mail_to': ('envelope__to', return_or_make_list),
        'subject': ('subject', as_is),
        'text': ('text', as_is),
        'html': ('html', as_is),
        'attachments': ('__self___get_attachments', stringify),
        'info': ('__self___get_info', stringify),
    }
    REDUCER = dict_reducer

    @property
    def _get_attachments_uploads(self):
        return [self.instance['attachment%s' % i] for i in range(1, self.instance['attachments'] + 1)]

    @property
    def _get_attachments(self):
        return {
            'count': self.instance['attachments'],
        }

    @property
    def _get_info(self):
        return {
            'charsets': self.instance['charsets'],
            'SPF': self.instance['SPF'],
            'envelope': self.instance['envelope'],
        }

    @property
    def required_json(self):
        response = super(CreateIncomingMail, self).required_json
        response.update({'meta': stringify(self.instance)})
        return response


class CreateActivityEvent(Serializer):
    BODY_MAP = {
        'name': ('event', as_is),
        'sg_event_id': ('sg_event_id', as_is),
        'sg_message_id': ('sg_message_id', lambda x: x.split('.filter')[0]),
        'timestamp': ('timestamp', datetime_from_timestamp),
        'smtp_id': ('smtp-id', as_is, False, 'stupid-sendgrid'),
        'category': ('category', as_is, False, 'stupid-sendgrid'),
        'email': ('email', as_is, False, 'stupid-sendgrid'),
    }
    REDUCER = dict_reducer

    @property
    def _get_attachments_uploads(self):
        return [self.instance['attachment%s' % i] for i in range(1, self.instance['attachments'] + 1)]

    @property
    def _get_attachments(self):
        return {
            'count': self.instance['attachments'],
        }

    @property
    def _get_info(self):
        return {
            'charsets': self.instance['charsets'],
            'SPF': self.instance['SPF'],
            'envelope': self.instance['envelope'],
        }

    @property
    def required_json(self):
        response = super(CreateActivityEvent, self).required_json
        response.update({'meta': stringify(self.instance)})
        return response
