import django_tables2 as tables
from django_tables2.utils import A

from businessflow.models import Task


class TaskTable(tables.Table):
    process = tables.TemplateColumn(
        template_name='widgets/tables2/task_process.html',
        verbose_name="Process"
    )
    code = tables.LinkColumn('businessflow-task-detail', args=[A('pk')])

    class Meta:
        model = Task
        fields = (
            'code',
            'name',
            'assigned_to',
            'process',
        )
        attrs = {"class": "table table-bordered table-condensed"}
