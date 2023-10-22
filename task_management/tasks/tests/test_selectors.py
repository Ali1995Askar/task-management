import datetime

from tasks.models import Task
from unittest import TestCase
from django.contrib.auth import get_user_model

from tasks.selectors import TaskSelectors

USER_MODEL = get_user_model()


class TestTaskSelectors(TestCase):
    def setUp(self) -> None:
        self.created_by_payload = {
            'first_name': 'ali',
            'last_name': 'askar',
            'email': 'ali1995askar@gmail.com',
            'username': 'ali_2_askar_2',
            'password': 'TestPassword12345'
        }

        self.assigned_to_payload = {
            'first_name': 'tonny',
            'last_name': 'liso',
            'email': 'tonny.liso.com',
            'username': 'tonny__2_liso_2',
            'password': 'TestPassword12345'
        }

        self.titles = 'Fix user management service bugs'
        self.description = 'when users try to login the site re-direct them to wrong url'
        self.status = ['TODO', 'IN_PROGRESS', 'DONE']
        self.created_by = USER_MODEL.objects.create_user(**self.created_by_payload)
        self.assigned_to = USER_MODEL.objects.create_user(**self.assigned_to_payload)
        self.today = datetime.date.today()

    def tearDown(self):
        USER_MODEL.objects.all().delete()
        Task.objects.all().delete()

    def test_get_task_count_for_user_by_date(self):
        Task.objects.create(
            title=self.titles,
            description=self.description,
            due_date=self.today + datetime.timedelta(days=1),
            assigned_to=self.assigned_to
        )
        for i in range(5):
            Task.objects.create(
                title=self.titles,
                description=self.description,
                due_date=datetime.date.today(),
                assigned_to=self.assigned_to
            )

        tasks_count = TaskSelectors.get_task_count_for_user_by_date(
            user=self.assigned_to,
            due_date=datetime.date.today())

        self.assertEqual(tasks_count, 5)

        tasks_count = TaskSelectors.get_task_count_for_user_by_date(
            user=self.assigned_to,
            due_date=self.today + datetime.timedelta(days=1))

        self.assertEqual(tasks_count, 1)

    def test_get_user_created_tasks(self):
        Task.objects.create(
            title=self.titles,
            description=self.description,
            due_date=self.today + datetime.timedelta(days=1),
            created_by=self.assigned_to
        )
        for i in range(5):
            Task.objects.create(
                title=self.titles,
                description=self.description,
                due_date=datetime.date.today(),
                created_by=self.created_by
            )

        tasks = TaskSelectors.get_user_created_tasks(user=self.created_by)
        self.assertEqual(tasks.count(), 5)

        tasks = TaskSelectors.get_user_created_tasks(user=self.assigned_to)
        self.assertEqual(tasks.count(), 1)

    def test_filter_tasks_for_user_created_or_assigned(self):

        Task.objects.create(
            title=self.titles,
            description=self.description,
            due_date=self.today + datetime.timedelta(days=1),
            created_by=self.assigned_to
        )
        for i in range(5):
            Task.objects.create(
                title=self.titles,
                description=self.description,
                due_date=datetime.date.today(),
                assigned_to=self.assigned_to
            )

        tasks = TaskSelectors.filter_tasks_for_user_created_or_assigned(user=self.assigned_to)
        self.assertEqual(tasks.count(), 6)

        tasks = TaskSelectors.filter_tasks_for_user_created_or_assigned(user=self.created_by)
        self.assertEqual(tasks.count(), 0)

        Task.objects.all().update(assigned_to=self.created_by)

        tasks = TaskSelectors.filter_tasks_for_user_created_or_assigned(user=self.created_by)
        self.assertEqual(tasks.count(), 6)

        tasks = TaskSelectors.filter_tasks_for_user_created_or_assigned(user=self.assigned_to)
        self.assertEqual(tasks.count(), 1)

        Task.objects.all().update(created_by=self.created_by)

        tasks = TaskSelectors.filter_tasks_for_user_created_or_assigned(user=self.created_by)
        self.assertEqual(tasks.count(), 6)

        tasks = TaskSelectors.filter_tasks_for_user_created_or_assigned(user=self.assigned_to)
        self.assertEqual(tasks.count(), 0)

        Task.objects.all().update(assigned_to=self.assigned_to)
        tasks = TaskSelectors.filter_tasks_for_user_created_or_assigned(user=self.created_by)
        self.assertEqual(tasks.count(), 6)

        tasks = TaskSelectors.filter_tasks_for_user_created_or_assigned(user=self.assigned_to)
        self.assertEqual(tasks.count(), 6)

    def test_search_by_title_or_description(self):

        Task.objects.create(
            title=self.titles,
            description=self.description,
            due_date=self.today + datetime.timedelta(days=1),
            created_by=self.assigned_to
        )
        for title in ['fix bugs', 'write-tests', 'deploy new service', 'backup db', 'fix tests']:
            Task.objects.create(
                title=title,
                description=f'{title} and some description',
                due_date=datetime.date.today(),
                created_by=self.assigned_to,
                assigned_to=self.created_by
            )
        fix_keyword = 'FIX'  # in-sensitive
        write_keyword = 'write'
        tasks = TaskSelectors.search_by_title_or_description(qs=Task.objects.all(), keyword=fix_keyword)
        self.assertEqual(tasks.count(), 3)

        for task in tasks:
            self.assertTrue('fix' in task.title.lower() or 'fix' in task.description.lower())
            self.assertTrue('fix' in task.title.lower() or 'fix' in task.description.lower())

        tasks = TaskSelectors.search_by_title_or_description(keyword=write_keyword, qs=Task.objects.all())
        self.assertEqual(tasks.count(), 1)
        task = tasks.first()
        self.assertTrue('write' in task.title.lower() or 'write' in task.description.lower())
        self.assertTrue('write' in task.title.lower() or 'write' in task.description.lower())

    def test_filter_by_status(self):
        for status in ['TODO', 'TODO', 'TODO', 'IN_PROGRESS', 'IN_PROGRESS', 'DONE']:
            Task.objects.create(
                title=status,
                description=f'{status} and some description',
                due_date=datetime.date.today(),
                status=status
            )

        todo_tasks = TaskSelectors.filter_by_status(qs=Task.objects.all(), status=Task.Status.TODO.value)
        self.assertEqual(todo_tasks.count(), 3)

        in_progress_tasks = TaskSelectors.filter_by_status(qs=Task.objects.all(), status=Task.Status.IN_PROGRESS.value)
        self.assertEqual(in_progress_tasks.count(), 2)

        done_tasks = TaskSelectors.filter_by_status(qs=Task.objects.all(), status=Task.Status.DONE.value)
        self.assertEqual(done_tasks.count(), 1)

        self.assertTrue(all(task.status == 'TODO' for task in todo_tasks))
        self.assertTrue(all(task.status == 'IN_PROGRESS' for task in in_progress_tasks))
        self.assertTrue(all(task.status == 'DONE' for task in done_tasks))
