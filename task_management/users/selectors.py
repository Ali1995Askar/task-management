from django.contrib.auth import get_user_model
from django.db.models import F, CharField, Value, When, Case, Q, QuerySet
from django.db.models.functions import Concat


class UserSelectors:
    @classmethod
    def get_users_full_names_if_exists_else_usernames(cls) -> QuerySet:
        users = get_user_model().objects.annotate(
            full_name=Case(
                When(
                    ~Q(first_name="") & ~Q(last_name=""),  # Check if first_name and last_name are not empty
                    then=Concat(F('first_name'), Value(' '), F('last_name'), output_field=CharField())
                ),
                default=F('username'),
                output_field=CharField(),
            )
        )

        user_names = users.values_list('id', 'full_name')
        return user_names
