#!/usr/bin/env python

import os
import datetime

# setup the environment
SETTINGS = 'example_leave.settings'
os.environ['DJANGO_SETTINGS_MODULE'] = SETTINGS

import django
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

from leave.models import(
    Employee,
    UserProfile,
    LeaveRequest
)


# Manager
jane_emp = Employee.objects.create(employee_number=101675, name='Jane')
jane_usr = User.objects.create_user('jane', 'jane@me.org', '1234')
jane_profile = UserProfile.objects.create(user=jane_usr, employee=jane_emp)

# requestor
john_emp = Employee.objects.create(
    employee_number=101450,
    name='John',
    reports_to=jane_emp
)
john_usr = User.objects.create_user('john', 'john@me.org', '1234')
john_profile = UserProfile.objects.create(
    user=john_usr,
    employee=john_emp
)

# HR manager
smith_emp = Employee.objects.create(
    employee_number=101131,
    name='Smith',
    reports_to=jane_emp
)
smith_usr = User.objects.create_user('smith', 'smith@me.org', '1234')
smith_profile = UserProfile.objects.create(
    user=smith_usr,
    employee=smith_emp
)


# Groups and Permissions
content_type = ContentType.objects.get_for_model(LeaveRequest)

# Manager Approver
manager = Group.objects.create(name='Manager')
manager_approve_perm = Permission.objects.create(
    codename='manager_approve',
    name='Can Manager approve',
    content_type=content_type
)
manager_approve_perm.group_set.add(manager)

# HR Approver
hr_approver = Group.objects.create(name='HR')
hr_approve_perm = Permission.objects.create(
    codename='hr_approve',
    name='Can HR approve leave request',
    content_type=content_type
)
hr_approve_perm.group_set.add(hr_approver)

# Assign users to group
jane_usr.groups.add(manager, )
smith_usr.groups.add(hr_approver)
