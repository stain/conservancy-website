from django.shortcuts import render_to_response

def view(request):
    """Conservancy campaign view

    Performs all object queries necessary to render the campaign page.
    """

    return render_to_response("campaign.html")
