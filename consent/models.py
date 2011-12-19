"""
There are two key models in the Consent app. These are Privilege and Consent.
A privilage is added to the website normally in the Django admin and then a
user has the option of granting the consent to to the website. After Consent
has been granted, the user is able to revoke the consent.
"""
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Privilege(models.Model):
    """
    A privilage is a permission that the website asks from the user. This
    could be the permission to email them, share the users details or to use
    their (already authorised) social netorking sites.
    """
    name = models.CharField(max_length=64)
    description = models.TextField()
    users = models.ManyToManyField(User, through='consent.Consent')

    class Meta:
        ordering = ['name', ]

    def __unicode__(self):
        return self.name

    def is_granted_by(self, user):
        consent = Consent.objects.get_or_none(user=user, privilege=self)
        if consent:
            return consent.is_granted
        return False


class ConsentManager(models.Manager):
    """
    The ConsentManager adds a number of utility methods to the Consent.objects
    interface to help with common tasks and functions.
    """

    def for_user(self, user):
        """
        Return the Consent instances for a given user.
        """
        return Consent.objects.filter(user=user)

    def grant_consent(self, user, privileges):
        """
        Grant an QuerySet (or iterable) of privileges for a specifiv user.
        """
        for privilege in privileges:
            consent, created = Consent.objects.get_or_create(
                user=user, privilege=privilege)
            if not created:
                consent.revoked = False
                consent.revoked_on = None
                consent.save()

    def revoke_consent(self, user, privileges):
        """
        Revoke an QuerySet (or iterable) of privileges for a specifiv user.
        """
        Consent.objects.filter(user=user, privilege__in=privileges).update(
                revoked=True, revoked_on=datetime.now())

    def granted(self, user=None):
        """
        Return all of the granted consents either for all users or the given
        user.
        """
        granted_consents = self.filter(revoked=False)
        if user:
            granted_consents = granted_consents.filter(user=user)
        return granted_consents

    def revoked(self, user=None):
        """
        Return all of the revoked consents either for all the users or the
        given user.
        """
        revoked_consents = self.filter(revoked=True)
        if user:
            revoked_consents = revoked_consents.filter(user=user)
        return revoked_consents

    def get_or_none(self, *args, **kwargs):

        try:
            return self.get(*args, **kwargs)
        except Consent.DoesNotExist:
            pass

        return None


class Consent(models.Model):
    """
    Consent is the agreement from a user to grant a specific privilege. This
    can then be revoked by the user at a later date.
    """
    user = models.ForeignKey(User)
    privilege = models.ForeignKey(Privilege)
    granted_on = models.DateTimeField(default=datetime.now)
    revoked_on = models.DateTimeField(null=True, blank=True)
    revoked = models.BooleanField(default=False)

    objects = ConsentManager()

    class Meta:
        unique_together = ('user', 'privilege',)
        ordering = ['privilege__name', ]

    def revoke(self):
        """
        Revoke the users consent for the Privilege if it has not already been
        revoked.
        """
        if not self.revoked:
            self.revoked = True
            self.revoked_on = datetime.now()

    def grant(self):
        """
        Grant the users consent for the Privilege if it has been revoked.
        """
        if self.revoked:
            self.revoked = False
            self.revoked_on = None
            self.granted_on = datetime.now()

    @property
    def is_granted(self):
        """
        Returns True if this consent has not been revoked by the user.
        Otherwise False is returned.
        """
        return not self.revoked

    @property
    def is_revoked(self):
        """
        returns True if this consent has been revoked by the user.
        Otherwise False is returned.
        """
        return not self.is_granted

    def __unicode__(self):

        if not self.revoked:
            adjv = 'permits'
        else:
            adjv = 'revoked'

        return "%s %s the '%s' privilege" % (self.user, adjv, self.privilege)
