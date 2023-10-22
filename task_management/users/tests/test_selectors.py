from django.test import Client
from django.test import TestCase
from users.selectors import UserSelectors
from django.contrib.auth import get_user_model

USER_MODEL = get_user_model()


class TestSelectors(TestCase):
    def setUp(self) -> None:
        self.user = {
            'first_name': 'ali',
            'last_name': 'askar',
            'email': 'ali1995askar@gmail.com',
            'username': 'ali_askar',
            'password': 'TestPassword12345'
        }

        self.client = Client()

    def test_get_users_full_names_if_exists_else_usernames(self):
        users = UserSelectors.get_users_full_names_if_exists_else_usernames()
        self.assertQuerysetEqual(users, [])
        self.current_user = USER_MODEL.objects.create_user(**self.user)
        _, name_to_display = UserSelectors.get_users_full_names_if_exists_else_usernames().first()

        self.assertEqual(name_to_display, 'ali askar')
        self.current_user.first_name = ""
        self.current_user.save()
        self.current_user.refresh_from_db()
        _, name_to_display = UserSelectors.get_users_full_names_if_exists_else_usernames().first()
        self.assertEqual(name_to_display, 'ali_askar')
