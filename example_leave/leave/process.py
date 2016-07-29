from django import forms
from businessflow.forms import ApprovalForm

from leave.handlers import(
    update_leaverequest_after_hr_approval,
    update_leaverequest_after_manager_approval
)


class HrApprovalForm(ApprovalForm):
    payment_settled = forms.TypedChoiceField(
        coerce=lambda x: x == 'True',
        choices=((False, 'No'), (True, 'Yes')),
        label='Payment Settled'
    )

    document_submitted = forms.TypedChoiceField(
        coerce=lambda x: x == 'True',
        choices=((False, 'No'), (True, 'Yes')),
        label='Payment Settled'
    )


PROCESS = {
    'initial': {
        'name': 'Manager Approval',
        'on_completion': [update_leaverequest_after_manager_approval],
        'group': 'Manager',
        'next_transition': 'hr_approver'
        # if 'form' is not defined, then busineesflow
        # will use default ApprovalForm
    },
    'hr_approver': {
        'form': HrApprovalForm,
        'name': 'HR Approval',
        'on_completion': [update_leaverequest_after_hr_approval],
        'group': 'HR'
    }
}
