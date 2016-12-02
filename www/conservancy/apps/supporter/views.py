import conservancy

def index(request):
    with conservancy.ParameterValidator(request.GET, 'upgrade_id') as validator:
        try:
            amount_param = float(request.GET['upgrade'])
        except (KeyError, ValueError):
            validator.fail()
        else:
            validator.validate('{.2f}'.format(amount_param))
    partial_amount = amount_param if validator.valid else 0
    context = {
        'partial_amount': partial_amount,
        'minimum_amount': 120 - partial_amount,
    }
    return conservancy.render_template_with_context(request, "supporter/index.html", context)
