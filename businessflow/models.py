from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import(
    GenericForeignKey,
    GenericRelation
)

from businessflow.forms import ApprovalForm


class Task(models.Model):
    name = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(max_length=100)
    assigned_to = models.ForeignKey(Group, related_name='tasks')
    is_closed = models.BooleanField(default=False)
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def code(self):
        """Unique identifier of task"""
        return "{}-{}".format(self.slug, self.id)

    @property
    def process_config(self):
        return self.content_object.PROCESS

    @property
    def state(self):
        return self.process_config[self.slug]

    @property
    def get_approval_form(self):
        return self.state.get('form', None) or ApprovalForm

    @property
    def next_transition(self):
        return self.state.get('next_transition', None)

    def submit(self, form, user):
        status = form.cleaned_data['status']
        comments = form.cleaned_data['remarks']

        self.is_closed = True
        self.save()

        Approval.objects.create(
            task=self,
            approval_by=user,
            status=status,
            comments=comments
        )

        # execute content object task action
        self.execute_task_actions(form)

        if self.next_transition:
            new_state = self.process_config[self.next_transition]
            self.create_new_task(new_state)

    def create_new_task(self, state):
        group = Group.objects.get(name=state['group'])

        Task.objects.create(
            name=state['name'],
            slug=self.next_transition,
            assigned_to=group,
            content_type=self.content_type,
            object_id=self.content_object.id
        )

    def execute_task_actions(self, form):
        task_actions = self.state['on_completion']
        for action in task_actions:
            action(form, self.content_object)


class Approval(models.Model):
    task = models.OneToOneField(Task, related_name='approval')
    approval_by = models.ForeignKey(
        User, blank=True, null=True, related_name='+')
    approval_on = models.DateTimeField(
        null=True,
        blank=True,
        auto_now_add=True
    )
    comments = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100, choices=[
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ])


class BusinessFlow(models.Model):
    tasks = GenericRelation(Task)

    class Meta:
        abstract = True

    def start_businessflow(self, initial_state=None):
        initial = initial_state or 'initial'
        state = self.PROCESS[initial]
        group = Group.objects.get(name=state['group'])
        content_type = ContentType.objects.get_for_model(self)

        Task.objects.create(
            name=state['name'],
            slug=initial,
            assigned_to=group,
            content_type=content_type,
            object_id=self.id
        )

