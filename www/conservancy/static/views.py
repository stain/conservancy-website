import os.path
from django.http import HttpResponse
from django.template import RequestContext, loader

def handler(request, errorcode):
    STATIC_ROOT = '/home/www/website/www/conservancy/static/'
    path = 'error/' + errorcode + '/index.html'
    fullpath = STATIC_ROOT + path
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

def index(request):
    # return HttpResponse("Hello, static world: " + request.get_full_path())
    path = request.get_full_path()
    path = path.lstrip('/')
    if path[-1:] == '/':
        path += 'index.html'
    STATIC_ROOT = '/home/www/website/www/conservancy/static/'
    fullpath = STATIC_ROOT + path
    if not os.path.exists(fullpath):
        # return HttpResponse("Sorry that's a 404: " + path)
        return handler404(request)
    template = loader.get_template(path)
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def debug(request):
    path = request.get_full_path()
    path = path.lstrip('/')
    return HttpResponse("Hello, static world: " + path)

