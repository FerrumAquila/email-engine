# Package Imports
from model_utils.models import TimeStampedModel

# Django Imports
from django.db.models import *


class AetosModel(TimeStampedModel):
    is_active = BooleanField(default=True)
    meta = TextField(default='{}')

    class Meta:
        abstract = True

    class Options:
        create_serialiser = None

    def serialise(self, data):
        pass

    @classmethod
    def create_from_webhook(cls, data):
        obj = cls(**cls.Options.create_serialiser(data).required_json)
        obj.save()
        return obj
