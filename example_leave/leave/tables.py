import django_tables2 as tables
from django_tables2.utils import A

from leave.models import LeaveRequest


class LeaveRequestTable(tables.Table):
    id = tables.LinkColumn(
        'leave-request-detail',
        args=[A('pk')],
        verbose_name="Request ID")

    status = tables.TemplateColumn(
        '<span class="label label-success">{{record.get_status_display}}</span>')

    class Meta:
        model = LeaveRequest
        fields = (
            'id',
            'leave_from',
            'leave_to',
            'created_on',
            'status'
        )
        attrs = {"class": "table table-bordered table-condensed"}
