from conservancy.apps.fundgoal.models import FundraisingGoal as FundraisingGoal

def fundgoal_lookup(fundraiser_sought):
    try:
        return FundraisingGoal.objects.get(fundraiser_code_name=fundraiser_sought)
    except FundraisingGoal.DoesNotExist:
        # we have no object!  do something
        return None

def sitefundraiser(request):
    return {'sitefundgoal': fundgoal_lookup('supporterrun') }
