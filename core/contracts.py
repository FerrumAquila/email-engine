# Packaged Imports
from core.resources.serialisers import *


class ParseIncomingMail(Serializer):
    BODY_MAP = {
        'persons': {
            '_from': ('mail_from', as_is),
            '_to': ('mail_to', return_or_make_list),
            '_cc': ('mail_cc', return_or_make_list),
        },
        'content': {
            'subject': ('subject', as_is),
            'text': ('text', as_is),
            'html': ('html', as_is),
        },
        'meta': ('info', jsonify),
    }
    REDUCER = instance_reducer


class SendEmailPostRequest(Serializer):
    BODY_MAP = {
        'customer_id': ('d__customer_id', str),
        '_from_email': ('d__from', str),
        '_to_email': ('d__to', str),
        'subject': ('d__subject', str),
        'content': ('d__content', unicode),
        'custom_args': ('__self___get_custom_args', return_or_make_list),
        'email_args': {
            'tenant_id': ('d__custom_args__tenant_id', str),
            'lci_id': ('d__custom_args__lci_id', str),
        },
        'async': ('d__async', read_true_false)
    }
    REDUCER = dict_reducer

    @property
    def _get_custom_args(self):
        return [{'key': key, 'value': str(value)} for key, value in self.instance['d']['custom_args'].items()]

