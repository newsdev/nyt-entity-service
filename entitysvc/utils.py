import os
import re

def get_env():
    return os.environ.get('DEPLOYMENT_ENVIRONMENT', 'dev')

def valid_uuid(possible_uuid):
    """
    Checks that a possible UUID4 string is a valid UUID4.
    """
    regex = re.compile('^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z', re.I)
    match = regex.match(possible_uuid)
    return bool(match)

def clean_payload(payload):
    """
    Serializes a payload from form strings to more useful Python types.
    `payload` is a dictionary where both keys and values are exclusively strings.
    * empty string becomes None
    * applies a true / false test to possible true / false string values.
    """
    output = {}
    for k,v in payload.items():

        # Takes the first value.
        v = v[0]

        # Serializes values
        if v == u'':
            v = None
        if v.lower() in ['true', 'yes', 'y', '1']:
            v = True
        if v.lower() in ['false', 'no', 'n', '0']:
            v = False

        # Values not in the test pass through.
        output[k] = v
    return output
