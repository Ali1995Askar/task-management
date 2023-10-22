from django.test import Client
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

SIGNIN_URL = reverse('users:signin')
SIGNUP_URL = reverse('users:signup')
SIGN_OUT_URL = reverse('users:sign-out')
CHANGE_PASSWORD_URL = reverse('users:change-password')

USER_MODEL = get_user_model()


class TestUsersViews(TestCase):
    def setUp(self) -> None:
        self.logged_user = {
            'first_name': 'ali',
            'last_name': 'askar',
            'email': 'ali1995askar@gmail.com',
            'username': 'ali_askar',
            'password': 'TestPassword12345'
        }

        self.other_user = {
            'first_name': 'other_user',
            'last_name': 'other_user',
            'email': 'other_user@gmail.com',
            'username': 'other_user',
            'password': 'otherTestPassword12345'
        }

        self.client = Client()
        self.current_user = USER_MODEL.objects.create_user(**self.logged_user)

    def tearDown(self):
        USER_MODEL.objects.all().delete()

    def test_get_signin(self):
        response = self.client.get(SIGNIN_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login to Your Account')

    def test_post_correct_signin(self):
        response = self.client.post(
            SIGNIN_URL,
            {
                'username': self.logged_user['username'],
                'password': self.logged_user['password']}
        )

        expected_redirect_url = reverse('tasks:list')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, expected_redirect_url)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_post_wrong_signin(self):
        response = self.client.post(SIGNIN_URL, {'username': self.logged_user['username'], 'password': 'wrong'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_get_signup_view(self):
        response = self.client.get(SIGNUP_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create an Account')

    def test_post_correct_signup(self):
        self.other_user['password1'] = self.other_user['password']
        self.other_user['password2'] = self.other_user['password']
        del self.other_user['password']

        self.assertEqual(USER_MODEL.objects.all().count(), 1)
        response = self.client.post(SIGNUP_URL, self.other_user)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/tasks/list/')
        # Should go to login page (after create user)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        # Two users Now
        self.assertEqual(USER_MODEL.objects.all().count(), 2)

    def test_post_wrong_signup(self):
        self.other_user['password1'] = 'weak'
        self.other_user['password2'] = 'weak'
        del self.other_user['password']

        self.assertEqual(USER_MODEL.objects.all().count(), 1)
        response = self.client.post(SIGNUP_URL, self.other_user)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create an Account')
        self.assertEqual(USER_MODEL.objects.all().count(), 1)

    def test_get_change_password(self):
        self.client.login(username='ali_askar', password='TestPassword12345')
        response = self.client.get(CHANGE_PASSWORD_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Change Password Form')

    def test_post_correct_change_password(self):
        login = self.client.login(username='ali_askar', password='TestPassword12345')
        self.assertTrue(login)

        payload = {
            'old_password': 'TestPassword12345',
            'new_password1': 'NewTestPassword12345',
            'new_password2': 'NewTestPassword12345',

        }

        response = self.client.post(CHANGE_PASSWORD_URL, payload)

        self.assertEqual(response.status_code, 302)

        login = self.client.login(username='ali_askar', password='TestPassword12345')
        self.assertFalse(login)

        login = self.client.login(username='ali_askar', password='NewTestPassword12345')
        self.assertTrue(login)

    def test_post_wrong_change_password(self):
        login = self.client.login(username='ali_askar', password='TestPassword12345')
        self.assertTrue(login)
        payload = {
            'old_password': 'wrongpassword',
            'new_password1': 'NewTestPassword12345',
            'new_password2': 'NewTestPassword12345',

        }
        response = self.client.post(CHANGE_PASSWORD_URL, payload)
        self.assertEqual(response.status_code, 200)
        login = self.client.login(username='ali_askar', password='TestPassword12345')
        self.assertTrue(login)

        login = self.client.login(username='ali_askar', password='NewTestPassword12345')
        self.assertFalse(login)

    def test_get_logout_view(self):
        self.client.login(username='ali_askar', password='TestPassword12345')
        response = self.client.get(SIGN_OUT_URL)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Are you sure you want to Logout ?')

    def test_post_logout(self):
        self.client.login(username='ali_askar', password='TestPassword12345')
        response = self.client.post(SIGN_OUT_URL)
        self.assertEqual(response.status_code, 302)
