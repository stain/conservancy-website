from django.shortcuts import render_to_response
from django import forms
from models import SummitRegistration

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
                                      {'form': form.cleaned_data})
    else:
        form = SummitForm()

    return render_to_response('summit_registration/register.html',
                              {'form': form})
