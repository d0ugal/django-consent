from django.http import HttpResponseRedirect
from django.views.generic import ListView, FormView

from consent.models import Privilege, Consent
from consent.forms import ConsentForm


class PrivilegeListView(ListView):
    """
    The PrivilegeListView inherits from ``django.views.generic.ListView`` and
    sets a number of defaults to make it easy to integrate into your app.
    """

    #: The template variable name for the QuerySet of ``consent.models.Privilege``
    context_object_name = 'privilege_list'
    #: The default template name for showing the list of privileges
    template_name = 'consent/privilege_list_view.html'
    model = Privilege


class ConsentEditView(FormView):

    #: The default template name for editing instances of ``consent.model.Consent``
    template_name = 'consent/consent_edit_view.html'
    form_class = ConsentForm
    success_url = '.'

    def get_privileges_with_consent(self):
        """
        Return all of the granted consents for the current user.
        """
        return Consent.objects.granted(user=self.request.user)

    def get_initial(self):
        """
        Create an initial data for the form of the consent ID's that the user
        has current granted.
        """
        consents = self.get_privileges_with_consent()
        consent_ids = consents.values_list('id', flat=True)
        return {'consents': consent_ids, }

    def form_valid(self, form):
        """
        Validate the form and update the users choices, granting and revoking
        privileges based on their choices.
        """

        current_consents = self.get_privileges_with_consent()
        consents = form.cleaned_data['consents']

        if consents:
            consent_ids = consents.values_list('id', flat=True)
        else:
            consent_ids = []
        revoked_privileges = current_consents.exclude(pk__in=consent_ids)
        Consent.objects.revoke_consent(self.request.user, revoked_privileges)

        if consents:
            current_consent_ids = current_consents.values_list('id', flat=True)
            consented_privileges = consents.exclude(pk__in=current_consent_ids)
            Consent.objects.grant_consent(self.request.user, consented_privileges)

        return HttpResponseRedirect(self.get_success_url())
