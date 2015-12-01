from django.shortcuts import render_to_response
from conservancy import context_processors as context_processors
from django.template import RequestContext
from django import forms
from django.template import RequestContext
from conervancy.apps.summit_registration.models import SummitRegistration

def register(request):
    """Summit registration form view
    """

    class SummitForm(ModelForm):
        class Meta:
            model = SummitRegistration

    SummitForm.base_fields['email'].label = 'Email address'
    SummitForm.base_fields['phone'].label = 'Phone number'
    SummitForm.base_fields['address'].label = 'Mailing address'
    SummitForm.base_fields['cle_credit'].label = 'Attending for CLE credit?'

    if request.method == 'POST':
        form = SummitForm(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response('summit_registration/register_success.html',
                                      {'form': form.cleaned_data}, context_instance=RequestContext(request))
    else:
        form = SummitForm()

    return render_to_response('summit_registration/register.html',
                              {'form': form}, context_instance=RequestContext(request))
