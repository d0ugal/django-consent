from django.test import Client, TestCase


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

        for privilege in Privilege.objects.all():

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
