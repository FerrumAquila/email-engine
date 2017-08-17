# App Imports
import webhooks
from core.resources.responses import success_response

# Django Imports
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


@csrf_exempt
@require_POST
def email_activities_webhook(request):
    if request.method == 'POST':
        webhooks.EmailActivities.process(request)
    return success_response('email activities received', dict())


@csrf_exempt
@require_POST
def incoming_mail_webhook(request):
    if request.method == 'POST':
        webhooks.IncomingMail.process(request)
    return success_response('incoming mail received', dict())
