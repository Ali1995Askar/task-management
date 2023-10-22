from tasks import forms
from tasks.models import Task
from django.views import generic
from tasks.services import TasksServices
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')
class ListTasksView(generic.ListView):
    template_name = 'tasks/list.html'
    context_object_name = 'tasks'
    queryset = Task.objects.all()

    def get_queryset(self):
        qs = TasksServices.get_user_tasks_with_search_filter(request=self.request)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = TasksServices.group_tasks_by_status(qs=context['tasks'])
        return context


@method_decorator(login_required, name='dispatch')
class CreateTaskView(generic.CreateView):
    model = Task
    form_class = forms.TaskForm
    template_name = 'tasks/create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object, form = TasksServices.check_if_user_can_accept_task(self.request, self.object, form)
        self.object.created_by = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("tasks:details", kwargs={'pk': self.object.pk})


@method_decorator(login_required, name='dispatch')
class TaskDetailsView(generic.DetailView):
    model = Task
    context_object_name = 'task'
    template_name = "tasks/details.html"

    def get_queryset(self):
        qs = TasksServices.get_user_connected_tasks(request=self.request)
        return qs


@method_decorator(login_required, name='dispatch')
class UpdateTaskView(generic.UpdateView):
    model = Task
    form_class = forms.TaskForm
    template_name = 'tasks/update.html'
    context_object_name = 'task'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object, form = TasksServices.check_if_user_can_accept_task(self.request, self.object, form)
        form.save()
        return super().form_valid(form)

    def get_queryset(self):
        qs = TasksServices.get_user_connected_tasks(request=self.request)
        return qs

    def get_success_url(self):
        return reverse_lazy('tasks:details', kwargs={'pk': self.object.id})


@method_decorator(login_required, name='dispatch')
class DeleteTaskView(generic.DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy("tasks:list")

    def get_queryset(self):
        qs = TasksServices.get_user_tasks(request=self.request)
        return qs
