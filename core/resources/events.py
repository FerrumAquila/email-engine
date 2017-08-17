# Package Imports
import pusher

# Django Imports
from django.conf import settings


class EventClient(object):
    try:
        CLIENT = pusher.Pusher(
            app_id=settings.EE_INTEGRATION['PUSHER_APP']['ID'],
            key=settings.EE_INTEGRATION['PUSHER_APP']['KEY'],
            secret=settings.EE_INTEGRATION['PUSHER_APP']['SECRET'],
            ssl=True
        )
    except Exception as e:
        CLIENT = None

    @classmethod
    def send_event(cls, channel_name, event_name, message):
        cls.CLIENT.trigger(channel_name, event_name, message)

    @classmethod
    def send_message(cls, channel_name, lci_id, body, posted_by=None, send_notification=False):
        if send_notification and posted_by:
            body = u'{posted_by}: {message}'.format(posted_by=posted_by, message=unicode(body))
        else:
            body = body

        cls.send_event(channel_name, u'new_message', {u'message': id, u'lci_id': lci_id, u'body': body})
