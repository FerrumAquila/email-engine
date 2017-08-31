# Packaged Imports
from core.resources.serialisers import *


class CreateSGMessageIdLink(Serializer):
    BODY_MAP = {
        'object_id': ('object_id', int),
        'object_type': ('object_type', as_is),
        'sg_message_id': ('sg_message_id', as_is),
    }
    REDUCER = dict_reducer
