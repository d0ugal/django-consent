from django.http import HttpResponseRedirect
from django.views.generic import ListView, FormView

from consent.models import Privilege, Consent
from consent.forms import ConsentForm


class PrivilegeListView(ListView):

    context_object_name = 'privilege_list'
    template_name = 'consent/privilege_list_view.html'
    model = Privilege


class PrivilegeEditView(FormView):

    context_object_name = 'consent_list'
    template_name = 'consent/consent_edit_view.html'
    form_class = ConsentForm
    success_url = '.'

    def get_privileges_with_consent(self):
        return Consent.objects.filter(user=self.request.user, revoked=False)

    def get_initial(self):
        consents = self.get_privileges_with_consent()
        consent_ids = consents.values_list('id', flat=True)
        return {'consents': consent_ids, }

    def form_valid(self, form):

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
