from django.db import models
from django.contrib.auth.models import User

from businessflow.models import BusinessFlow
from leave import process


class Employee(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    employee_number = models.IntegerField(unique=True)

    reports_to = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        related_name='children'
    )
    email = models.EmailField(blank=True, null=True)


class UserProfile(models.Model):
    """convenience class to relate employee to user."""
    user = models.OneToOneField(User, related_name='profile')
    employee = models.OneToOneField('Employee', related_name='profile')

    @property
    def user_groups(self):
        return self.user.groups.all().values_list('name', flat=True)


class LeaveRequest(BusinessFlow):
    # assign your process here
    PROCESS = process.PROCESS

    employee = models.ForeignKey(
        Employee,
        blank=True,
        null=True,
        related_name='leave_requests'
    )
    leave_type = models.CharField(
        max_length=50,
        choices=[
            ('S', 'Sick'),
            ('V', 'Vacation'),
            ('W', 'Wedding / Marriage'),
        ]
    )
    leave_from = models.DateTimeField()
    leave_to = models.DateTimeField()

    # for HR role
    payment_settled = models.BooleanField(default=False)
    document_submitted = models.BooleanField(default=False)

    reason = models.TextField(blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True, null=True)
    created_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name='+'
    )
    status = models.CharField(
        max_length=40,
        blank=True,
        null=True,
        choices=[
            ('created', 'Created'),
            ('submitted_for_approval', 'Submitted for approval'),
            ('manager_approved', 'Manager Approved'),
            ('manager_rejected', 'Manager Rejected'),
            ('hr_approved', 'HR Approved'),
            ('hr_rejected', 'HR Rejected')
        ]
    )

    def code(self):
        return "LVREQ-{}".format(self.id)

    def submit_for_approval(self):
        self.status = "submitted_for_approval"
        self.save()

        # start business flow
        # this will create task for initial state which
        # you defined in your PROCESS config
        self.start_businessflow()
