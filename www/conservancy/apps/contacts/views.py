from django.shortcuts import render_to_response
from django import forms
from models import ContactEntry
from django.forms import ModelForm

def subscribe(request):
    """Mailing list subscription form
    """

    class ContactEntryForm(ModelForm):
        class Meta:
            model = ContactEntry

    ContactEntryForm.base_fields['subscribe_sflc'].label = 'Receive Software Freedom Law Center updates'
    ContactEntryForm.base_fields['subscribe_sfc'].label = 'Receive Software Freedom Conservancy updates'

    if request.method == 'POST':
        form = ContactEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return render_to_response('contacts/subscribe_success.html',
                                      {'form': form.cleaned_data})
    else:
        form = ContactEntryForm()

    return render_to_response('contacts/subscribe.html',
                              {'form': form})
