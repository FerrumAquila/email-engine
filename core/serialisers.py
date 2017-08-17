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


class CreateSGMessageIdLink(Serializer):
    BODY_MAP = {
        'object_id': ('object_id', int),
        'object_type': ('object_type', as_is),
        'sg_message_id': ('sg_message_id', as_is),
    }
    REDUCER = dict_reducer
