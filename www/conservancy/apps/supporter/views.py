import conservancy

def index(request):
    partial_amount = conservancy.param_if_valid(request.GET, 'upgrade', 'upgrade_id', 0)
    context = {
        'partial_amount': partial_amount,
        'minimum_amount': 120 - partial_amount,
    }
    return conservancy.render_template_with_context(request, "supporter/index.html", context)
