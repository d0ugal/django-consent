from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class Privilege(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    users = models.ManyToManyField(User, through='consent.Consent')

    class Meta:
        ordering = ['name', ]

    def __unicode__(self):
        return self.name


class ConsentManager(models.Manager):

    def for_user(self, user):
        return Consent.objects.filter(user=user)

    def grant_consent(self, user, privileges):
        for privilege in privileges:
            consent, created = Consent.objects.get_or_create(
                user=user, privilege=privilege)
            if not created:
                consent.revoked = False
                consent.revoked_on = None
                consent.save()

    def revoke_consent(self, user, privileges):
        Consent.objects.filter(user=user, privilege__in=privileges).update(
                revoked=True, revoked_on=datetime.now())


class Consent(models.Model):
    user = models.ForeignKey(User)
    privilege = models.ForeignKey(Privilege)
    granted_on = models.DateTimeField(default=datetime.now)
    revoked_on = models.DateTimeField(null=True, blank=True)
    revoked = models.BooleanField(default=False)

    objects = ConsentManager()

    class Meta:
        unique_together = ('user', 'privilege',)

    def __unicode__(self):

        if self.revoked:
            adjv = 'permits'
        else:
            adjv = 'revoked'

        return "%s %s the '%s' privilege" % (self.user, adjv, self.privilege)
