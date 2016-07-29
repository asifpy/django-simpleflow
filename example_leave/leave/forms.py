from django import forms

from leave.models import LeaveRequest


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = [
            'leave_from',
            'leave_to',
            'leave_type',
            'reason'
        ]
