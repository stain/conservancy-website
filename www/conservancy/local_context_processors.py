import conservancy.settings
from conservancy.apps.fundgoal.models import FundraisingGoal as FundraisingGoal

def fundgoal_lookup(fundraiser_sought):
    try:
        return FundraisingGoal.objects.get(fundraiser_code_name=fundraiser_sought)
    except FundraisingGoal.DoesNotExist:
        # we have no object!  do something
        return None

def sitefundraiser(request):
    return {'sitefundgoal': fundgoal_lookup('fy-2018-main-match') }

if conservancy.settings.FORCE_CANONICAL_HOSTNAME:
    _HOST_URL_VAR = {'host_url': 'https://' + conservancy.settings.FORCE_CANONICAL_HOSTNAME}
    def host_url(request):
        return _HOST_URL_VAR
else:
    def host_url(request):
        return {'host_url': request.build_absolute_uri('/').rstrip('/')}
