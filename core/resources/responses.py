# Django Imports
from django.http import JsonResponse

success_response = lambda m, d: JsonResponse(data={'success': 1, 'message': m, 'data': d})
failure_response = lambda e, d: JsonResponse(data={'success': 0, 'error': e, 'data': d})
