# App Imports
import utils
import models
import webhooks
from core.resources import events

# Package Imports
from annoying.functions import get_object_or_None

# Django Imports
from django.dispatch import receiver


@receiver(webhooks.signals.webhook_pinged, sender=webhooks.EmailActivities)
def activities_received(sender, **kwargs):
    mixed_request_datas = kwargs['request_data']
    print "\n\n\nactivities_received signal received for request_datas"
    print mixed_request_datas

    grouped_request_datas = utils.EmailActivitiesHandler.group_by_tenant_id(mixed_request_datas)
    for tenant_id, request_datas in grouped_request_datas.items():
        unique_email_object_ids = list()
        for request_data in request_datas:
            activity = models.ActivityEvent.create_from_webhook(request_data)

            if activity.sg_message_id not in unique_email_object_ids:
                unique_email_object_ids.append(activity.sg_message_id)

        for email_object_id in unique_email_object_ids:
            status = utils.EmailActivitiesHandler.get_latest_status(email_object_id)
            email_object_people_id_link = get_object_or_None(models.SGMessageIdLink, sg_message_id=email_object_id)
            if email_object_people_id_link:
                people_id = email_object_people_id_link.object_id
                channel = 'tenant_id' + tenant_id + '-email_activities-' + str(people_id)
                events.EventClient.send_event(channel, u'new_email_activity', status)


@receiver(webhooks.signals.webhook_pinged, sender=webhooks.IncomingMail)
def redirect_noreply(sender, **kwargs):
    request_data = kwargs['request_data']
    print "\n\n\nredirect_noreply signal received for request_data"
    print request_data

    incoming_mail = models.IncomingMail.create_from_webhook(request_data)
    notification_text = '%s<br>%s<br>%s' % (
        utils.IncomingMailHandler.email_from_text(incoming_mail),
        utils.IncomingMailHandler.open_email_button(incoming_mail),
        utils.IncomingMailHandler.reply_email_help_text(incoming_mail)
    )
    meta_params = utils.IncomingMailHandler.get_params_from_email(incoming_mail)
    tenant_id = meta_params['tenant_id']
    lci_id = meta_params['lci_id']
    channel = 'tenant_id' + tenant_id + "-lc_channel-" + str(lci_id)
    events.EventClient.send_message(channel, lci_id, notification_text)
