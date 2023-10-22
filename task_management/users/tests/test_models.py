from django.test import Client
from django.test import TestCase
from users.models import Profile
from django.contrib.auth import get_user_model

USER_MODEL = get_user_model()


class TestProfileMode(TestCase):
    def setUp(self) -> None:
        self.user = {
            'first_name': 'ali',
            'last_name': 'askar',
            'email': 'ali1995askar@gmail.com',
            'username': 'ali_askar',
            'password': 'TestPassword12345'
        }

        self.client = Client()

    def test_signal_dispatch_when_create_user(self):
        self.assertEqual(Profile.objects.all().count(), 0)
        self.current_user = USER_MODEL.objects.create_user(**self.user)
        self.assertEqual(Profile.objects.all().count(), 1)
        self.assertEqual(Profile.objects.first().user, self.current_user)
        self.assertEqual(Profile.objects.first().max_tasks_per_day, 10)
        self.current_user.delete()
        self.assertEqual(Profile.objects.all().count(), 0)
        self.assertEqual(USER_MODEL.objects.all().count(), 0)
