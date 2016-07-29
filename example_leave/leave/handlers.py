
def update_leaverequest_after_manager_approval(form, leaverequest):
    """This function will get trigger after manager approval.
    Use this function for appropriate state in PROCESS config(process.py).
    """
    status = form.cleaned_data['status']

    leaverequest.status = "manager_{}".format(status)
    leaverequest.save()


def update_leaverequest_after_hr_approval(form, leaverequest):
    """This function will get trigger after manager approval.
    HR approval form has some additional which needs to be popuated in LR
    Use this function for appropriate state in PROCESS config(process.py).
    """
    status = form.cleaned_data['status']
    document_submitted = form.cleaned_data['document_submitted']
    payment_settled = form.cleaned_data['payment_settled']

    leaverequest.status = "hr_{}".format(status)
    leaverequest.document_submitted = document_submitted
    leaverequest.payment_settled = payment_settled
    leaverequest.save()
