from datetime import datetime

from django.contrib.auth.models import User
from fixture_generator import fixture_generator

from consent.models import Consent, Privilege


@fixture_generator(User)
def test_users():
    User.objects.create_user(username="john", email="john@test.com",
        password="password")
    User.objects.create_user(username="smith", email="smith@test.com",
        password="password")


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


@fixture_generator(Consent, requires=['test_consent.test_privileges',
    'test_consent.test_users'])
def test_consents():

    privileges = Privilege.objects.order_by('name')

    newsletter, marketing, facebook, twitter = privileges

    john = User.objects.get(username='john')
    smith = User.objects.get(username='smith')

    Consent.objects.create(user=smith, privilege=newsletter)
    Consent.objects.create(user=smith, privilege=marketing,
        granted_on=datetime(2011, 11, 01), revoked_on=datetime(2011, 11, 01),
        revoked=True)
    Consent.objects.create(user=smith, privilege=facebook)

    Consent.objects.create(user=john, privilege=newsletter,
        granted_on=datetime(2011, 10, 01), revoked_on=datetime(2011, 10, 01),
        revoked=True)
    Consent.objects.create(user=john, privilege=marketing)
    Consent.objects.create(user=john, privilege=facebook)
