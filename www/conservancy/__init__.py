from django.shortcuts import render_to_response
from django.template import RequestContext

def render_template_with_context(request, template_path, context_dict):
    return render_to_response(template_path, context_dict,
                              context_instance=RequestContext(request))
