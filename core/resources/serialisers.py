# Packaged Imports
from aetos_serialiser.serialisers import Serializer
from aetos_serialiser.helpers import instance_reducer, dict_reducer

# Django Imports
import json
import datetime

# TODO "Vishesh": add below helper lambdas in aetos_serialiser
# from aetos_serialiser.helpers.lambdas import return_or_make_list, as_is
as_is = lambda x: x
jsonify = lambda x: json.loads(x)
stringify = lambda x: json.dumps(x)
return_or_make_list = lambda x: [x] if not isinstance(x, list) else x
datetime_from_timestamp = lambda x: datetime.datetime.fromtimestamp(x)
