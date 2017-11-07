from django.shortcuts import render
from django import forms
from conservancy.apps.contacts.models import ContactEntry
from django.forms import ModelForm

def subscribe(request):
    """Mailing list subscription form
    """

    class ContactEntryForm(ModelForm):
        class Meta:
            model = ContactEntry

    ContactEntryForm.base_fields['subscribe_conservancy'].label = 'Receive Software Freedom Conservancy updates'

    if request.method == 'POST':
        form = ContactEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'contacts/subscribe_success.html', {'form': form.cleaned_data})
    else:
        form = ContactEntryForm()

    return render(request, 'contacts/subscribe.html', {'form': form})
