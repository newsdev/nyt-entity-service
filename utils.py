import os
import re
import importlib

def get_env():
    return os.environ.get('DEPLOYMENT_ENVIRONMENT', 'dev')

settings = importlib.import_module('config.%s.settings' % get_env())

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

def get_page(request):
    try:
        page = int(request.args.get('page', '1'))
    except TypeError:
        page = 1

    return page

def paginate(request, obj_count, page, context):
    context['page'] = page

    total_pages = int(obj_count) // int(settings.ITEMS_PER_PAGE)
    remainder = int(obj_count) % int(settings.ITEMS_PER_PAGE)

    if remainder > 0:
        total_pages += 1

    previous_page = page - 1
    next_page = page + 1
    has_next = True
    has_previous = True

    if previous_page < 1:
        previous_page = 1
        has_previous = False

    if next_page > total_pages:
        next_page = total_pages
        has_next = False

    last_item = page * settings.ITEMS_PER_PAGE

    if not has_next:
        last_item = obj_count

    if not has_previous:
        first_item = 1

    else:
        first_item = (settings.ITEMS_PER_PAGE * (page - 1)) + 1

    context['pagination'] = {
        'last_item': last_item,
        'first_item': first_item,
        'remainder': remainder,
        'total': obj_count,
        'has_next': has_next,
        'has_previous': has_previous,
        'page': page,
        'total_pages': total_pages,
        'previous_page_number': previous_page,
        'next_page_number': next_page,
        'pages': list(range(1,total_pages + 1))
    }

    return context

def build_context(request):
    """
    We needed some static context for our pages and
    you won't believe what happened next.
    """
    context = {}
    context['user_email'] = request.environ.get('HTTP_X_GOOG_AUTHENTICATED_USER_EMAIL', None) or 'test@test.dev'
    return context
