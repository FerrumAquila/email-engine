# App Imports
import utils
import models
from core.resources import responses

# Django Imports
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def email_latest_status(request, people_id):
    people_message_id_link = models.SGMessageIdLink.objects.filter(object_id=people_id, object_type='people')
    if people_message_id_link:
        object_id = people_message_id_link.latest('id').sg_message_id
        status = utils.EmailActivitiesHandler.get_latest_status(object_id)
        return responses.success_response('email latest status', status)
    return responses.failure_response('email latest status not found', {'status': 'unknown'})


@csrf_exempt
def incoming_mail_data(request, pk):
    incoming_mail = models.IncomingMail.objects.get(pk=pk)
    incoming_mail_json = utils.IncomingMailHandler.get_data_json(incoming_mail)
    return responses.success_response('incoming mail data', incoming_mail_json)


def email_info(request, email_id):
    info = utils.EmailHandler.fetch_lite(email_id)
    person = info.copy()
    person.pop('response')
    return responses.success_response('received', person)
