from django.db import models
from django.conf import settings

from core.utils import AbstractBaseModel


class Profile(AbstractBaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    max_tasks_per_day = models.IntegerField(default=10)

    def __str__(self):
        return f'{self.user}: max tasks: {self.max_tasks_per_day}'
