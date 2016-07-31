===================
django-businessflow
===================


This is a work-in-progress code branch of `django-simpleflow` as a third-party app, which aims to bring generic workflow engine for `Django`.

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
		'businessflow'
	}

	PROJECT_NAME = 'YOUR PROJECT NAME'
