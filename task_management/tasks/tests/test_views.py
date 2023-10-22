import datetime
from django.test import Client
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from tasks.models import Task

USER_MODEL = get_user_model()


class TestTasksListView(TestCase):
    def setUp(self) -> None:
        self.logged_user = {
            'first_name': 'ali',
            'last_name': 'askar',
            'email': 'ali1995askar@gmail.com',
            'username': 'ali_askar',
            'password': 'TestPassword12345'
        }

        self.client = Client()
        self.current_user = USER_MODEL.objects.create_user(**self.logged_user)
        self.client.login(username='ali_askar', password='TestPassword12345')

    def test_get_empty_list_tasks(self):
        url = reverse('tasks:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'My Tasks')

        todo_tasks = response.context.get('todo_tasks')
        in_progress_tasks = response.context.get('in_progress_tasks')
        done_tasks = response.context.get('done_tasks')

        self.assertEqual(todo_tasks.count(), 0)
        self.assertEqual(in_progress_tasks.count(), 0)
        self.assertEqual(done_tasks.count(), 0)

    def test_get_list_tasks_with_data(self):
        url = reverse('tasks:list')
        for title in ['fix bugs', 'write-tests', 'deploy new service', 'backup db', 'fix tests']:
            Task.objects.create(
                title=title,
                description=f'{title} and some description',
                due_date=datetime.date.today(),
                created_by=self.current_user,
                assigned_to=self.current_user
            )
        response = self.client.get(url)
        todo_tasks = response.context.get('todo_tasks')
        in_progress_tasks = response.context.get('in_progress_tasks')
        done_tasks = response.context.get('done_tasks')
        self.assertEqual(todo_tasks.count(), 5)
        self.assertEqual(in_progress_tasks.count(), 0)
        self.assertEqual(done_tasks.count(), 0)

        tasks = Task.objects.all()[:2]
        for task in tasks:
            task.status = Task.Status.IN_PROGRESS
            task.save()

        tasks = Task.objects.all()[2:4]
        for task in tasks:
            task.status = Task.Status.DONE
            task.save()

        response = self.client.get(url)
        todo_tasks = response.context.get('todo_tasks')
        in_progress_tasks = response.context.get('in_progress_tasks')
        done_tasks = response.context.get('done_tasks')
        self.assertEqual(todo_tasks.count(), 1)
        self.assertEqual(in_progress_tasks.count(), 2)
        self.assertEqual(done_tasks.count(), 2)

    def test_get_list_tasks_with_data_and_filter(self):
        base_url = reverse('tasks:list')
        for title in ['fix bugs', 'write-tests', 'deploy new service', 'backup db', 'fix tests']:
            for status in ['TODO', 'IN_PROGRESS', 'DONE']:
                Task.objects.create(
                    title=title,
                    description=f'{title} and some description',
                    due_date=datetime.date.today(),
                    status=status,
                    created_by=self.current_user,
                    assigned_to=self.current_user)

        query_params = {'filter': 'TODO'}

        url = base_url + '?' + '&'.join([f'{k}={v}' for k, v in query_params.items()])
        response = self.client.get(url)

        todo_tasks = response.context.get('todo_tasks')
        in_progress_tasks = response.context.get('in_progress_tasks')
        done_tasks = response.context.get('done_tasks')
        self.assertEqual(todo_tasks.count(), 5)
        self.assertEqual(in_progress_tasks.count(), 0)
        self.assertEqual(done_tasks.count(), 0)

        query_params = {'filter': 'IN_PROGRESS'}
        url = base_url + '?' + '&'.join([f'{k}={v}' for k, v in query_params.items()])
        response = self.client.get(url)
        todo_tasks = response.context.get('todo_tasks')
        in_progress_tasks = response.context.get('in_progress_tasks')
        done_tasks = response.context.get('done_tasks')
        self.assertEqual(todo_tasks.count(), 0)
        self.assertEqual(in_progress_tasks.count(), 5)
        self.assertEqual(done_tasks.count(), 0)

        query_params = {'filter': 'DONE'}
        url = base_url + '?' + '&'.join([f'{k}={v}' for k, v in query_params.items()])
        response = self.client.get(url)
        todo_tasks = response.context.get('todo_tasks')
        in_progress_tasks = response.context.get('in_progress_tasks')
        done_tasks = response.context.get('done_tasks')
        self.assertEqual(todo_tasks.count(), 0)
        self.assertEqual(in_progress_tasks.count(), 0)
        self.assertEqual(done_tasks.count(), 5)

    def test_get_list_tasks_with_data_and_search_and_filter(self):
        base_url = reverse('tasks:list')
        for title in ['fix bugs', 'write-tests', 'deploy new service', 'backup db', 'fix tests']:
            for status in ['TODO', 'IN_PROGRESS', 'DONE']:
                Task.objects.create(
                    title=title,
                    description=f'{title} and some description',
                    due_date=datetime.date.today(),
                    status=status,
                    created_by=self.current_user,
                    assigned_to=self.current_user)

        query_params = {'search': ''}
        url = base_url + '?' + '&'.join([f'{k}={v}' for k, v in query_params.items()])
        response = self.client.get(url)
        todo_tasks = response.context.get('todo_tasks')
        in_progress_tasks = response.context.get('in_progress_tasks')
        done_tasks = response.context.get('done_tasks')
        self.assertEqual(todo_tasks.count(), 5)
        self.assertEqual(in_progress_tasks.count(), 5)
        self.assertEqual(done_tasks.count(), 5)

        query_params = {'search': '', 'filter': ''}
        url = base_url + '?' + '&'.join([f'{k}={v}' for k, v in query_params.items()])
        response = self.client.get(url)
        todo_tasks = response.context.get('todo_tasks')
        in_progress_tasks = response.context.get('in_progress_tasks')
        done_tasks = response.context.get('done_tasks')
        self.assertEqual(todo_tasks.count(), 5)
        self.assertEqual(in_progress_tasks.count(), 5)
        self.assertEqual(done_tasks.count(), 5)

        query_params = {'search': 'fix'}
        url = base_url + '?' + '&'.join([f'{k}={v}' for k, v in query_params.items()])
        response = self.client.get(url)
        todo_tasks = response.context.get('todo_tasks')
        in_progress_tasks = response.context.get('in_progress_tasks')
        done_tasks = response.context.get('done_tasks')
        self.assertEqual(todo_tasks.count(), 2)
        self.assertEqual(in_progress_tasks.count(), 2)
        self.assertEqual(done_tasks.count(), 2)

        query_params = {'search': 'fix', 'filter': 'TODO'}
        url = base_url + '?' + '&'.join([f'{k}={v}' for k, v in query_params.items()])
        response = self.client.get(url)
        todo_tasks = response.context.get('todo_tasks')
        in_progress_tasks = response.context.get('in_progress_tasks')
        done_tasks = response.context.get('done_tasks')
        self.assertEqual(todo_tasks.count(), 2)
        self.assertEqual(in_progress_tasks.count(), 0)
        self.assertEqual(done_tasks.count(), 0)

        query_params = {'search': 'deploy', 'filter': 'TODO'}
        url = base_url + '?' + '&'.join([f'{k}={v}' for k, v in query_params.items()])
        response = self.client.get(url)
        todo_tasks = response.context.get('todo_tasks')
        in_progress_tasks = response.context.get('in_progress_tasks')
        done_tasks = response.context.get('done_tasks')
        self.assertEqual(todo_tasks.count(), 1)
        self.assertEqual(in_progress_tasks.count(), 0)
        self.assertEqual(done_tasks.count(), 0)

        query_params = {'search': 'deploy', 'filter': 'IN_PROGRESS'}
        url = base_url + '?' + '&'.join([f'{k}={v}' for k, v in query_params.items()])
        response = self.client.get(url)
        todo_tasks = response.context.get('todo_tasks')
        in_progress_tasks = response.context.get('in_progress_tasks')
        done_tasks = response.context.get('done_tasks')
        self.assertEqual(todo_tasks.count(), 0)
        self.assertEqual(in_progress_tasks.count(), 1)
        self.assertEqual(done_tasks.count(), 0)

        query_params = {'search': 'deploy', 'filter': 'DONE'}
        url = base_url + '?' + '&'.join([f'{k}={v}' for k, v in query_params.items()])
        response = self.client.get(url)
        todo_tasks = response.context.get('todo_tasks')
        in_progress_tasks = response.context.get('in_progress_tasks')
        done_tasks = response.context.get('done_tasks')
        self.assertEqual(todo_tasks.count(), 0)
        self.assertEqual(in_progress_tasks.count(), 0)
        self.assertEqual(done_tasks.count(), 1)


class TestTasksCreateView(TestCase):
    def setUp(self) -> None:
        self.logged_user = {
            'first_name': 'ali',
            'last_name': 'askar',
            'email': 'ali1995askar@gmail.com',
            'username': 'ali_askar',
            'password': 'TestPassword12345'
        }

        self.client = Client()
        self.current_user = USER_MODEL.objects.create_user(**self.logged_user)
        self.client.login(username='ali_askar', password='TestPassword12345')

    def test_get_create_task(self):
        url = reverse('tasks:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task Create Form')

    def test_post_create_task(self):
        url = reverse('tasks:create')
        for title in ['fix bugs', 'write-tests', 'deploy new service', 'backup db', 'fix tests']:
            Task.objects.create(
                title=title,
                description=f'{title} and some description',
                due_date=datetime.date.today(),
                created_by=self.current_user,
                assigned_to=self.current_user
            )

        self.task_payload = {
            'title': 'new tasks from test',
            'description': f'{title} and some description',
            'due_date': datetime.date.today(),
            'status': Task.Status.IN_PROGRESS.value,
            'assigned_to': self.current_user.id
        }

        self.assertEqual(Task.objects.all().count(), 5)
        response = self.client.post(url, self.task_payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.all().count(), 6)

        profile = self.current_user.profile
        profile.max_tasks_per_day = 6
        profile.save()

        self.task_payload['title'] = 'test no more than 6 assigned to ali'

        self.assertEqual(Task.objects.all().count(), 6)
        response = self.client.post(url, self.task_payload)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.all().count(), 7)
        tasks = Task.objects.filter(assigned_to__isnull=True)
        self.assertEqual(tasks.count(), 1)
        self.assertEqual(tasks.first().title, 'test no more than 6 assigned to ali')

        tasks = Task.objects.filter(assigned_to=self.current_user)
        self.assertEqual(tasks.count(), 6)

        profile = self.current_user.profile
        profile.max_tasks_per_day = 7
        profile.save()
        self.client.post(url, self.task_payload)
        tasks = Task.objects.filter(assigned_to=self.current_user)
        self.assertEqual(tasks.count(), 7)

        self.client.post(url, self.task_payload)
        tasks = Task.objects.filter(assigned_to=self.current_user)
        self.assertEqual(tasks.count(), 7)

        self.task_payload['due_date'] = datetime.date.today() + datetime.timedelta(days=1)
        self.client.post(url, self.task_payload)
        tasks = Task.objects.filter(assigned_to=self.current_user)
        self.assertEqual(tasks.count(), 8)


class TestTaskUpdateView(TestCase):
    def setUp(self) -> None:
        self.logged_user = {
            'first_name': 'ali',
            'last_name': 'askar',
            'email': 'ali1995askar@gmail.com',
            'username': 'ali_askar',
            'password': 'TestPassword12345'
        }

        self.client = Client()
        self.current_user = USER_MODEL.objects.create_user(**self.logged_user)
        self.client.login(username='ali_askar', password='TestPassword12345')
        self.object = Task.objects.create(title='fix bugs',
                                          description='fix bugs and some description',
                                          due_date=datetime.date.today(),
                                          created_by=self.current_user,
                                          assigned_to=self.current_user
                                          )

    def test_get_create_task(self):
        url = reverse('tasks:update', kwargs={'pk': self.object.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['task'].pk, self.object.pk)
        self.assertContains(response, 'Task Update Form')
        self.assertContains(response, 'fix bugs')

    def test_post_update_task(self):
        url = reverse('tasks:update', kwargs={'pk': self.object.pk})
        response = self.client.post(url, data={
            'title': 'updated fix bugs',
            'description': 'updated fix bugs and some description',
            'due_date': datetime.date.today() + datetime.timedelta(days=1),
            'assigned_to': self.current_user.pk,
            'status': 'IN_PROGRESS',
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.all().count(), 1)

        self.object.refresh_from_db()
        self.assertEqual(self.object.title, 'updated fix bugs')
        self.assertEqual(self.object.description, 'updated fix bugs and some description')
        self.assertEqual(self.object.due_date, datetime.date.today() + datetime.timedelta(days=1))
        self.assertEqual(self.object.assigned_to, self.current_user)

    def test_not_created_or_assigned_no_access(self):
        url = reverse('tasks:update', kwargs={'pk': self.object.pk})
        self.object.assigned_to = None
        self.object.created_by = None
        self.object.save()
        response = self.client.post(url, data={
            'title': 'updated fix bugs',
            'description': 'updated fix bugs and some description',
            'due_date': datetime.date.today() + datetime.timedelta(days=1),
            'assigned_to': self.current_user.pk,
            'status': 'IN_PROGRESS',
        })
        self.assertEqual(response.status_code, 404)

        response = self.client.get(url, )
        self.assertEqual(response.status_code, 404)

    def test_cant_assign_to_user_with_limit_assigned_tasks(self):
        url = reverse('tasks:update', kwargs={'pk': self.object.pk})

        profile = self.current_user.profile
        profile.max_tasks_per_day = 0
        profile.save()

        response = self.client.post(url, data={
            'title': 'second update fix bugs',
            'description': 'updated fix bugs and some description',
            'due_date': datetime.date.today() + datetime.timedelta(days=1),
            'assigned_to': self.current_user.pk,
            'status': 'IN_PROGRESS',
        })
        self.assertEqual(response.status_code, 302)

        self.object.refresh_from_db()
        self.assertEqual(self.object.title, 'second update fix bugs')
        self.assertIsNone(self.object.assigned_to)


class TestTaskDeleteView(TestCase):
    def setUp(self) -> None:
        self.logged_user = {
            'first_name': 'ali',
            'last_name': 'askar',
            'email': 'ali1995askar@gmail.com',
            'username': 'ali_askar',
            'password': 'TestPassword12345'
        }

        self.client = Client()
        self.current_user = USER_MODEL.objects.create_user(**self.logged_user)
        self.client.login(username='ali_askar', password='TestPassword12345')
        self.object = Task.objects.create(title='fix bugs',
                                          description='fix bugs and some description',
                                          due_date=datetime.date.today(),
                                          created_by=self.current_user,
                                          assigned_to=self.current_user
                                          )

    def test_get_delete_task(self):
        url = reverse('tasks:delete', kwargs={'pk': self.object.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['task'].pk, self.object.pk)

        self.assertContains(response, 'Delete Task')
        self.assertContains(response, self.object.pk)

    def test_not_created_no_access(self):
        url = reverse('tasks:delete', kwargs={'pk': self.object.pk})
        self.object.created_by = None
        self.object.save()

        self.assertEqual(Task.objects.all().count(), 1)

        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Task.objects.all().count(), 1)

    def test_post_delete_successfully(self):
        url = reverse('tasks:delete', kwargs={'pk': self.object.pk})

        self.assertEqual(Task.objects.all().count(), 1)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.all().count(), 0)


class TestTaskDetailsView(TestCase):
    def setUp(self) -> None:
        self.logged_user = {
            'first_name': 'ali',
            'last_name': 'askar',
            'email': 'ali1995askar@gmail.com',
            'username': 'ali_askar',
            'password': 'TestPassword12345'
        }

        self.client = Client()
        self.current_user = USER_MODEL.objects.create_user(**self.logged_user)
        self.client.login(username='ali_askar', password='TestPassword12345')
        self.object = Task.objects.create(title='fix bugs',
                                          description='fix bugs and some description',
                                          due_date=datetime.date.today(),
                                          created_by=self.current_user,
                                          assigned_to=self.current_user
                                          )

    def test_get_task_details(self):
        url = reverse('tasks:details', kwargs={'pk': self.object.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['task'].pk, self.object.pk)
        self.assertContains(response, 'Task Details')
        self.assertContains(response, self.object.pk)

    def test_not_created_or_assigned_no_access(self):
        url = reverse('tasks:details', kwargs={'pk': self.object.pk})
        self.object.assigned_to = None
        self.object.created_by = None
        self.object.save()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
