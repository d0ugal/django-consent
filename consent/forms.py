from django import forms

from consent.models import Privilege


class PrivilegeForm(forms.ModelForm):

    class Meta:
        model = Privilege


class ConsentForm(forms.Form):
    consents = forms.ModelMultipleChoiceField(Privilege.objects,
        widget=forms.CheckboxSelectMultiple, required=False)
