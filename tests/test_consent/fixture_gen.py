from datetime import datetime

from django.contrib.auth.models import User
from fixture_generator import fixture_generator

from consent.models import Consent, Privilege


@fixture_generator(User)
def test_users():
    User.objects.create(username="john")
    User.objects.create(username="smith")


@fixture_generator(Privilege)
def test_privileges():
    Privilege.objects.create(name="Email Newsletter", description="""
    Send a bi-monthly news letter to the user.
    """)
    Privilege.objects.create(name="Marketing Emails", description="""
    Allow us to give your email address to third party spammers.
    """)
    Privilege.objects.create(name="Post to Facebook", description="""
    Send an update to Facebook when you upload a new picture.
    """)
    Privilege.objects.create(name="Post to Twitter", description="""
    Send an update to Twitter when you upload a new picture.
    """)


@fixture_generator(Consent, requires=['test_consent.test_privileges', ])
def test_consents():

    newsletter, marketing, facebook, twitter = Privilege.objects.order_by('name')

    smith, john = User.objects.order_by('username')

    Consent.objects.create(user=smith, privilege=newsletter)
    Consent.objects.create(user=smith, privilege=marketing,
        granred_on=datetime(2011, 11, 01), revoked_on=datetime(2011, 11, 01),
        revoked=True)
    Consent.objects.create(user=smith, privilege=facebook)

    Consent.objects.create(user=john, privilege=newsletter,
        granred_on=datetime(2011, 10, 01), revoked_on=datetime(2011, 10, 01),
        revoked=True)
    Consent.objects.create(user=john, privilege=marketing)
    Consent.objects.create(user=john, privilege=facebook)
