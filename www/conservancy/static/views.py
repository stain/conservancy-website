import mimetypes
import os.path
from django.http import HttpResponse
from django.template import RequestContext, loader
from conservancy.apps.fundgoal.models import FundraisingGoal as FundraisingGoal

STATIC_ROOT = os.path.abspath(os.path.dirname(__file__))
FILESYSTEM_ENCODING = 'utf-8'

def handler(request, errorcode):
    path = os.path.join('error', errorcode, 'index.html')
    fullpath = os.path.join(STATIC_ROOT, path)
    if not os.path.exists(fullpath):
        return HttpResponse("Internal error: " + path)
    template = loader.get_template(path)
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def handler401(request):
    return handler(request, '401')

def handler403(request):
    return handler(request, '403')

def handler404(request):
    return handler(request, '404')

def handler500(request):
    return handler(request, '500')

def fundgoal_lookup(fundraiser_sought):
    try:
        return FundraisingGoal.objects.get(fundraiser_code_name=fundraiser_sought)
    except FundraisingGoal.DoesNotExist:
     # we have no object!  do something
        return None

def index(request, *args, **kwargs):
    path = request.path.lstrip(u'/')
    if path.endswith(u'/'):
        path += u'index.html'
    try:
        path_bytes = path.encode(FILESYSTEM_ENCODING)
    except UnicodeEncodeError:
        # If the path can't be expressed on the filesystem, it must not exist.
        return handler404(request)
    fullpath = os.path.join(STATIC_ROOT, path_bytes)
    if not os.path.exists(fullpath):
        return handler404(request)
    content_type, _ = mimetypes.guess_type(path)
    if content_type != 'text/html':
        content = open(fullpath)
    else:
        content_type = None  # Let Django use its default
        template = loader.get_template(path)

        kwargs = kwargs.copy()
        if kwargs.has_key('fundraiser_sought'):
            kwargs['fundgoal'] = fundgoal_lookup(kwargs['fundraiser_sought'])

        kwargs['sitefundgoal'] = fundgoal_lookup('supporterrun')

        context = RequestContext(request, kwargs)
        content = template.render(context)
    return HttpResponse(content, content_type)

def debug(request):
    path = request.get_full_path()
    path = path.lstrip('/')
    return HttpResponse("Hello, static world: " + path)

