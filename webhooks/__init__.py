# App Imports
import serialisers
from signals import webhook_pinged

# Packaged Imports
import json
import cgi
from StringIO import StringIO as IO


class BaseWebHook(object):

    SIGNAL = webhook_pinged

    @classmethod
    def _emit_signal(cls, data):
        cls.SIGNAL.send(sender=cls, request_data=data)

    @classmethod
    def _parse_request(cls, request):
        """
        extract data from request object
        :param request: django view request object
        :return: extracted request data from request object
        """
        raise NotImplementedError('Implement Incoming Data Parser')

    @classmethod
    def _process_data(cls, request_data):
        """
        implement request data serialisation
        :param request_data: json data from webhook request
        :return: serialised data
        """
        raise NotImplementedError('Implement Processing Data')

    @classmethod
    def process(cls, request):
        request_data = cls._parse_request(request)
        processed_data = cls._process_data(request_data)
        cls._emit_signal(processed_data)
        return processed_data


class IncomingMail(BaseWebHook):

    IGNORE_KEYS = ['dkim']

    @classmethod
    def _parse_request(cls, request):
        parsed = cgi.FieldStorage(
            IO(request.body),
            headers={'content-type': 'multipart/form-data; boundary=xYzZY'},
            environ={'REQUEST_METHOD': 'POST'}
        )
        response_json = dict()
        for key in parsed:
            if key not in cls.IGNORE_KEYS:
                value = parsed[key].file.read()
                if value.startswith('{'):
                    value = json.loads(value)
                response_json.update({key: value})
        return response_json

    @classmethod
    def _process_data(cls, request_data):
        return request_data


class EmailActivities(BaseWebHook):

    @classmethod
    def _parse_request(cls, request):
        return json.loads(request.body)

    @classmethod
    def _process_data(cls, request_data):
        return request_data
