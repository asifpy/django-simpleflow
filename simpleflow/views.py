from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import DetailView
from django.contrib import messages
from django.conf import settings
from django.db import transaction
# from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import LoginRequiredMixin

from django_tables2 import SingleTableView

from simpleflow.models import Task
from simpleflow.tables import TaskTable


class TaskListView(LoginRequiredMixin, SingleTableView):
    template_name = 'tasks/task_list.html'
    model = Task
    context_object_name = 'tasks'
    context_table_name = 'tasks_table'
    table_pagination = {"per_page": 15}

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        context['project_name'] = getattr(
            settings, 'PROJECT_NAME', 'BUSINESSFLOW')
        return context

    def get_status(self):
        status = self.request.GET.get('status')
        if status == 'completed':
            return True
        else:
            return False

    def get_queryset(self):
        groups = self.request.user.groups.all().values_list('name', flat=True)
        tasks = self.model.objects.filter(
            assigned_to__name__in=groups,
            is_closed=self.get_status()
        )
        return tasks

    def get_table_class(self):
        return TaskTable


class TaskDetailView(LoginRequiredMixin, DetailView):
    template_name = 'tasks/task_detail.html'
    model = Task
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super(
            TaskDetailView, self).get_context_data(**kwargs)
        context['approval_form'] = self.task.get_approval_form
        return context

    @property
    def task(self):
        return self.get_object()

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = self.task.get_approval_form(request.POST)

        if form.is_valid():
            self.task.submit(
                form,
                request.user
            )

            msg = 'Task status updated successfully'
            messages.success(self.request, msg)
        else:
            msg = 'Approval form is not valid'
            messages.error(self.request, msg)

        return HttpResponseRedirect(
            reverse('simpleflow-task-detail',
                    args=[self.task.id]))
