from django import forms
from tasks.models import Task
from users.selectors import UserSelectors


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].widget = forms.Select(
            attrs={
                'class': 'form-control',
                'name': 'assigned_to',
                'id': 'assigned_to',
            },
            choices=UserSelectors.get_users_full_names_if_exists_else_usernames(),
        )

    class Meta:
        model = Task
        exclude = ['created_by']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'name': 'title',
                'id': 'title',
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'name': 'description',
                'id': 'description',
            }),

            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'name': 'due_date',
                'id': 'due_date',
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
                'name': 'status',
                'id': 'status',
            }),

        }
