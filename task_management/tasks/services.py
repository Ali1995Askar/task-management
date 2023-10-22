from typing import Tuple, Dict

from django.db.models import QuerySet

from tasks.models import Task
from tasks.forms import TaskForm
from tasks.selectors import TaskSelectors
from django.contrib.auth import get_user_model
from django.core.handlers.wsgi import WSGIRequest

User = get_user_model()


class TasksServices:
    @classmethod
    def check_if_user_can_accept_task(cls, request: WSGIRequest, obj: Task, form: TaskForm) -> Tuple[Task, TaskForm]:
        user: User = request.user
        tasks_count = TaskSelectors.get_task_count_for_user_by_date(user=obj.assigned_to, due_date=obj.due_date)

        if tasks_count >= user.profile.max_tasks_per_day:
            form.assigned_to = None
            obj.assigned_to = None

        return obj, form

    @classmethod
    def get_user_tasks(cls, request: WSGIRequest) -> QuerySet[Task]:
        user: User = request.user
        tasks = TaskSelectors.get_user_created_tasks(user=user)
        return tasks

    @classmethod
    def get_user_connected_tasks(cls, request):
        user: User = request.user
        qs = TaskSelectors.filter_tasks_for_user_created_or_assigned(user=user)
        return qs

    @classmethod
    def get_user_tasks_with_search_filter(cls, request) -> QuerySet[Task]:
        user: User = request.user
        keyword: str = request.GET.get('search')
        status: str = request.GET.get('filter')
        qs = TaskSelectors.filter_tasks_for_user_created_or_assigned(user=user)

        if status in Task.Status.values:
            qs = TaskSelectors.filter_by_status(qs=qs, status=status)

        if keyword:
            qs = TaskSelectors.search_by_title_or_description(qs=qs, keyword=keyword)

        return qs

    @classmethod
    def group_tasks_by_status(cls, qs: QuerySet[Task]) -> Dict[str, QuerySet[Task]]:
        tasks_dict = {
            'todo_tasks': TaskSelectors.filter_by_status(qs=qs, status=Task.Status.TODO.value),
            'in_progress_tasks': TaskSelectors.filter_by_status(qs=qs, status=Task.Status.IN_PROGRESS.value),
            'done_tasks': TaskSelectors.filter_by_status(qs=qs, status=Task.Status.DONE.value),
        }

        return tasks_dict
