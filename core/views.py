# App Imports
import utils
import models
import contracts
from core.resources import responses

# Package Imports
import json

# Django Imports
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def email_latest_status(request, people_id):
    people_message_id_link = models.SGMessageIdLink.objects.filter(object_id=people_id, object_type='people_id')
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


@csrf_exempt
def send_email(request):
    request_json = json.loads(request.body)
    email_dict = contracts.SendEmailPostRequest(request_json).required_json
    m, response = utils.EmailHandler.send_email(**email_dict)
    sg_message_id = response.headers.get('X-Message-Id')
    for args in email_dict['custom_args']:
        models.SGMessageIdLink.create_from_request({
            'object_type': args['key'],
            'object_id': args['value'],
            'sg_message_id': sg_message_id
        })
    d = {'sg_message_id': sg_message_id}
    return responses.success_response(m, d)
