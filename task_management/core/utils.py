import uuid
from functools import wraps
from django.db import models
from django.shortcuts import redirect


def anonymous_user_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return view_func(request, *args, **kwargs)

    return _wrapped_view


class Utils:

    @staticmethod
    def uuid4() -> str:
        rnd = str(uuid.uuid4())
        return rnd


class AbstractBaseModel(models.Model):
    class Meta:
        abstract = True
        ordering = ['-created_on_datetime']

    id = models.CharField(max_length=36, primary_key=True, default=Utils.uuid4, editable=False)
    created_on_datetime = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_on_datetime = models.DateTimeField(auto_now=True, db_index=True)
