import datetime

from django.test import Client
from django.test import TestCase
from users.models import Profile
from django.contrib.auth import get_user_model
from tasks.models import Task

USER_MODEL = get_user_model()


class TestTaskSModel(TestCase):
    def setUp(self) -> None:
        self.created_by_user = {
            'first_name': 'ali',
            'last_name': 'askar',
            'email': 'ali1995askar@gmail.com',
            'username': 'ali_askar',
            'password': 'TestPassword12345'
        }

        self.assigned_to_user = {
            'first_name': 'tonny',
            'last_name': 'liso',
            'email': 'tonny.liso.com',
            'username': 'tonny__liso',
            'password': 'TestPassword12345'
        }

        self.title = 'Fix user management service bugs'
        self.description = 'when users try to login the site re-direct them to wrong url'
        self.created_by = USER_MODEL.objects.create_user(**self.created_by_user)
        self.assigned_to = USER_MODEL.objects.create_user(**self.assigned_to_user)

    def tearDown(self):
        USER_MODEL.objects.all().delete()
        Task.objects.all().delete()

    def test_create_task(self):
        self.assertEqual(Task.objects.all().count(), 0)
        task_payload = {
            'title': self.title,
            'description': self.description,
            'due_date': datetime.date.today(),
            'created_by': self.created_by,
            'assigned_to': self.assigned_to,

        }
        Task.objects.create(**task_payload)
        self.assertEqual(Task.objects.all().count(), 1)
        obj = Task.objects.first()
        self.assertEqual(obj.title, self.title)
        self.assertEqual(obj.description, self.description)
        self.assertEqual(obj.due_date, datetime.date.today())
        self.assertEqual(obj.created_by, self.created_by)
        self.assertEqual(obj.assigned_to, self.assigned_to)
        self.assertEqual(obj.status, Task.Status.TODO.value)

    def test_task_nullable_fields(self):
        self.assertEqual(Task.objects.all().count(), 0)
        task_payload = {
            'title': self.title,
            'description': self.description,
            'due_date': datetime.date.today(),
            'status': 'IN_PROGRESS',
        }
        Task.objects.create(**task_payload)
        self.assertEqual(Task.objects.all().count(), 1)
        obj = Task.objects.first()
        self.assertEqual(obj.title, self.title)
        self.assertEqual(obj.description, self.description)
        self.assertEqual(obj.due_date, datetime.date.today())
        self.assertIsNone(obj.created_by)
        self.assertIsNone(obj.assigned_to)
        self.assertEqual(obj.status, Task.Status.IN_PROGRESS.value)
