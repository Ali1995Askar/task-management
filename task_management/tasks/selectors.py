from datetime import date
from tasks.models import Task
from django.db.models import QuerySet, Q
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskSelectors:

    @classmethod
    def get_task_count_for_user_by_date(cls, user: User, due_date: date) -> int:
        tasks_count = Task.objects.filter(assigned_to=user, due_date=due_date).count()
        return tasks_count

    @classmethod
    def get_user_created_tasks(cls, user: User) -> QuerySet[Task]:
        tasks = Task.objects.filter(created_by=user)
        return tasks

    @classmethod
    def filter_tasks_for_user_created_or_assigned(cls, user: User) -> QuerySet[Task]:
        tasks = Task.objects.filter(Q(created_by=user) | Q(assigned_to=user))
        return tasks

    @classmethod
    def search_by_title_or_description(cls, qs: QuerySet[Task], keyword) -> QuerySet[Task]:
        qs = qs.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword))
        return qs

    @classmethod
    def filter_by_status(cls, qs: QuerySet[Task], status: str) -> QuerySet[Task]:
        qs = qs.filter(status=status)
        return qs
