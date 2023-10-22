from datetime import date
from django.db import models
from django.conf import settings
from core.utils import AbstractBaseModel


class Task(AbstractBaseModel):
    class Status(models.Choices):
        TODO = 'TODO'
        IN_PROGRESS = 'IN_PROGRESS'
        DONE = 'DONE'

    status = models.CharField(max_length=25, choices=Status.choices, db_index=True, default=Status.TODO)
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    due_date = models.DateField(default=date.today, db_index=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)

    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    null=True,
                                    blank=True,
                                    on_delete=models.SET_NULL,
                                    related_name='assigned_tasks')

    def __str__(self):
        return f'{self.title} - {self.status}'
