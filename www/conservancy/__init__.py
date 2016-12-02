import hashlib

from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

HASH_ENCODING = 'utf-8'

def render_template_with_context(request, template_path, context_dict):
    return render_to_response(template_path, context_dict,
                              context_instance=RequestContext(request))

def param_if_valid(params, param_name, hash_param_name, default=None):
    try:
        seed = settings.CONSERVANCY_SECRET_KEY
        param_value = params[param_name]
        param_bytes = param_value.encode(HASH_ENCODING)
        given_hash = params[hash_param_name]
    except (AttributeError, KeyError, UnicodeEncodeError):
        return default
    good_hash = hashlib.sha256()
    good_hash.update(seed)
    good_hash.update(param_bytes)
    if given_hash == unicode(good_hash.hexdigest()):
        return param_value
    else:
        return default
