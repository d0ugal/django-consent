from django.test import Client, TestCase


class ModelsTestCase(TestCase):

    fixtures = ['consents.json', ]

    def setUp(self):

        from django.contrib.auth.models import User

        self.john = User.objects.get(username='john')
        self.smith = User.objects.get(username='smith')

    def test_module_util_methods(self):

        from consent.models import Consent

        granted = Consent.objects.granted()
        revoked = Consent.objects.revoked()

        for consent in granted:
            self.assertNotIn(consent, revoked)

        for consent in revoked:
            self.assertNotIn(consent, granted)

    def test_consent(self):

        from consent.models import Consent

        consents = Consent.objects.for_user(self.john)

        # the three that John has previously encoutered in the fixtures
        newsletter, marketing, facebook = consents

        msg = "john permits the 'Email Newsletter' privilege"
        self.assertEqual(str(newsletter), msg)
        msg = "john revoked the 'Marketing Emails' privilege"
        self.assertEqual(str(marketing), msg)

        self.assertNotIn(newsletter, Consent.objects.revoked(self.john))
        # Called twice, to test the falsey if in revoke
        newsletter.revoke()
        newsletter.revoke()
        newsletter.save()
        self.assertIn(newsletter, Consent.objects.revoked(self.john))

        self.assertNotIn(marketing, Consent.objects.granted(self.john))
        # Called twice, to test the falsey if in grant.
        marketing.grant()
        marketing.grant()
        marketing.save()
        self.assertIn(marketing, Consent.objects.granted(self.john))

    def test_checking_privileges(self):

        from consent.models import Privilege, Consent

        privileges = Privilege.objects.order_by('name')

        newsletter, marketing, facebook, twitter = privileges

        # Normal grants
        self.assertTrue(newsletter.is_granted_by(self.john))
        self.assertTrue(facebook.is_granted_by(self.john))

        # Granted and then revoked
        consent = Consent.objects.get(privilege=marketing, user=self.john)
        self.assertEqual(consent.is_revoked, True)

        self.assertFalse(marketing.is_granted_by(self.john))

        # Never granted, no consent exists.
        with self.assertRaises(Consent.DoesNotExist):
            Consent.objects.get(privilege=twitter, user=self.john)

        self.assertFalse(twitter.is_granted_by(self.john))


class ViewTestCase(TestCase):

    fixtures = ['consents.json', ]

    def setUp(self):

        from django.contrib.auth.models import User

        self.client = Client()
        self.client.login(username='john', password='password')
        self.john = User.objects.get(username='john')
        self.smith = User.objects.get(username='smith')

    def test_list_privilges(self):

        from consent.models import Privilege

        r = self.client.get('/')

        self.assertEqual(r.status_code, 200,
            "Response returned a %s when 200 was expected" % r.status_code)

        for privilege in Privilege.objects.filter(consent__user=self.john):

            self.assertIn(privilege.name, r.content)
            self.assertIn(privilege.description, r.content)

    def test_edit_consents(self):

        from consent.models import Consent

        r = self.client.get('/edit/')

        self.assertEqual(r.status_code, 200,
            "Response returned a %s when 200 was expected" % r.status_code)

        # Fixtures have the user john with 2 granted
        granted_count = Consent.objects.granted(user=self.john).count()
        self.assertEqual(granted_count, 2,
            "User %s John is expected to have 2 consents in the fixtures")
        revoked_count = Consent.objects.revoked(user=self.john).count()
        self.assertEqual(revoked_count, 1,
            "User %s John is expected to have 2 consents in the fixtures")

        # Posting an empty list, is just like selecting none and thus revoking
        # all.
        r = self.client.post('/edit/', {'consents': [], })

        granted_count = Consent.objects.granted(user=self.john).count()
        self.assertEqual(granted_count, 0)
        revoked_count = Consent.objects.revoked(user=self.john).count()
        self.assertEqual(revoked_count, 3)

        # Grant all of the consents
        r = self.client.post('/edit/', {'consents': [1, 2, 3, 4]})

        granted_count = Consent.objects.granted(user=self.john).count()
        self.assertEqual(granted_count, 4)
        revoked_count = Consent.objects.revoked(user=self.john).count()
        self.assertEqual(revoked_count, 0)
