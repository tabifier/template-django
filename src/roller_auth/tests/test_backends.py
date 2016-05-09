from django.test import TestCase

from nose.plugins.attrib import attr
from test_utils.factories import UserFactory, UserEmailFactory

from roller_auth.backends import EmailBackend


@attr('unit')
class TestEmailBackend(TestCase):

    def setUp(self):
        pass

    def test_active_user_with_valid_password(self):
        backend = EmailBackend()
        credentials = {'email': 'test@example.com', 'password': 'pass@word1'}
        user = UserFactory(**credentials)
        self.assertEqual(backend.authenticate(**credentials), user)

    def test_email_exists(self):
        backend = EmailBackend()
        credentials = {'email': 'test@example.com', 'password': 'pass@word1'}
        UserFactory(**credentials)
        self.assertIsNone(backend.authenticate(email=credentials['email'], password='invalid'))

    def test_inactive_email(self):
        backend = EmailBackend()
        credentials = {'email': 'test@example.com', 'password': 'pass@word1'}
        user = UserFactory(**credentials)
        user.is_active = False
        user.save()
        self.assertIsNone(backend.authenticate(**credentials))

    def test_invalid_account(self):
        backend = EmailBackend()
        self.assertIsNone(backend.authenticate(email='test@invalid.com'))

    def test_login_with_secondary_email(self):
        backend = EmailBackend()
        credentials = {'email': 'test@example.com', 'password': 'pass@word1'}
        user = UserFactory(**credentials)
        UserEmailFactory(user=user, email='test@example.io')

        self.assertEqual(backend.authenticate(email='test@example.io', password='pass@word1'), user)
