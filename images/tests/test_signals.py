from django.test import TestCase
import mock
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class CreateAuthTokenTest(TestCase):
    def test_cache(self):
        with mock.patch('images.signals.create_auth_token', autospec=True) as mocked_handler:
            post_save.connect(mocked_handler, sender=User)
            User.objects.create(username='admin', password='password')
            self.assertEquals(mocked_handler.call_count, 1)
