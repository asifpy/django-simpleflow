from django import forms
from django.utils.translation import ugettext_lazy as _


class ApprovalForm(forms.Form):
    status = forms.ChoiceField(
        label=_('Approval Status'),
        choices=[
            ('approved', 'Approved'),
            ('rejected', 'Rejected')
        ])

    remarks = forms.CharField(
        label=_('Remarks'),
        required=False,
        widget=forms.Textarea,
    )
