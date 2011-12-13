from django.test import Client, TestCase


class ModelsTestCase(TestCase):

    fixtures = ['consents.json', ]

    def setUp(self):

        from django.contrib.auth.models import User

        self.john = User.objects.get(username='john')
        self.smith = User.objects.get(username='smith')

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
        newsletter.revoke()
        newsletter.save()
        self.assertIn(newsletter, Consent.objects.revoked(self.john))

        self.assertNotIn(marketing, Consent.objects.granted(self.john))
        marketing.grant()
        marketing.save()
        self.assertIn(marketing, Consent.objects.granted(self.john))


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
