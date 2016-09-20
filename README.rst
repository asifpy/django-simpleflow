===================
django-simpleflow
===================


This is a work-in-progress code branch of `django-simpleflow` as a third-party app, which aims to bring generic workflow engine using `Django`.

Prerequisites
-------------
- Django 1.8+
- Python 2.7+, 3.2+
- Django Tables2

Usage
-----

**Add "simpleflow" to INSTALLED_APPS**

.. code-block:: python

	INSTALLED_APPS = {
		...
		'django_tables2',
		'simpleflow'
	}

	PROJECT_NAME = 'YOUR PROJECT NAME'

**Define your process with its states**

.. code-block:: python
	
	from leave.handlers import(
    	update_leaverequest_after_hr_approval,
    	update_leaverequest_after_manager_approval
	)

	PROCESS = {
    	'initial': {
        	'name': 'Manager Approval',
        	'on_completion': [update_leaverequest_after_manager_approval],
        	'group': 'Manager',
        	'next_transition': 'hr_approver'
        	# if 'form' is not defined, then simpleflow
        	# will use default ApprovalForm
    	},
    	'hr_approver': {
        	'form': HrApprovalForm,
        	'name': 'HR Approval',
        	'on_completion': [update_leaverequest_after_hr_approval],
        	'group': 'HR'
    	}
    }

**Assign the above defined process to the model**

.. code-block:: python

	from simpleflow.models import SimpleFlow
	from leave import process

	class LeaveRequest(SimpleFlow):
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

    	# trigger simpleflow
    	def submit_for_approval(self):
    		self.status = "submitted_for_approval"
    		self.save()

    		# start simpleflow
    		# this will create task for initial state which
    		# you defined in your PROCESS config
    		self.start_simpleflow()


