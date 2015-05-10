from conservancy.apps.fundgoal.models import FundraisingGoal
from django.shortcuts import get_object_or_404, render_to_response
from django.http import JsonResponse


def view(request):
    """JSON version of request
    """
    keysForJSON = [ 'fundraiser_goal_amount', 'fundraiser_so_far_amount', 'fundraiser_donation_count',
                    'fundraiser_donation_count_disclose_threshold' ]
    GET = request.GET
    codeNames =  []
    if 'code_name' in GET: codeNames += GET.getlist('code_name')

    returnDict = {}
    for fundGoal in FundraisingGoal.objects.filter(fundraiser_code_name__in=codeNames):
        codeName = fundGoal.fundraiser_code_name
        returnDict[codeName] = {}
        for kk in keysForJSON:
            if hasattr(codeName, kk):
                returnDict[codeName][kk] = getattr(fundGoal, kk)

    return JsonResponse( returnDict)
