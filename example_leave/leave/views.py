from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.views import generic
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin

from django_tables2 import SingleTableView

from leave.models import LeaveRequest
from leave.tables import LeaveRequestTable
from leave.forms import LeaveRequestForm


class LeaveRequestListView(LoginRequiredMixin, SingleTableView):
    login_url = '/auth/login/'
    template_name = 'leaverequest_list.html'
    model = LeaveRequest
    table_class = LeaveRequestTable
    context_object_name = 'leave_requests'
    context_table_name = 'leaverequest_table'
    table_pagination = {"per_page": 15}

    def get_queryset(self):
        employee = self.request.user.profile.employee
        requests = self.model.objects.filter(
            employee=employee
        )
        return requests


class LeaveRequestCreateUpdateView(object):
    def get_success_url(self):
        return reverse_lazy(
            'leave-request-detail',
            args=[self.object.id]
        )


class LeaveRequestCreateView(
    LoginRequiredMixin,
    LeaveRequestCreateUpdateView,
    generic.CreateView
):
    template_name = 'leaverequest_create.html'
    form_class = LeaveRequestForm
    model = LeaveRequest

    def form_valid(self, form):
        self.object = form.save(commit=False)
        employee = self.request.user.profile.employee
        self.object.employee = employee
        self.object.created_by = self.request.user
        self.object.status = 'created'
        self.object.save()

        msg = 'Leave Request created successfully for Badge: {}'.format(
            self.object.employee.name)
        messages.success(self.request, msg)

        return HttpResponseRedirect(self.get_success_url())


class LeaveRequestUpdateView(LeaveRequestCreateUpdateView, generic.UpdateView,
                             LoginRequiredMixin):
    template_name = 'leaverequest_update.html'
    form_class = LeaveRequestForm
    model = LeaveRequest


class LeaveRequestDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'leaverequest_detail.html'
    model = LeaveRequest
    context_object_name = 'leaverequest'


@transaction.atomic
def approval_submit(request, pk):
    leave_req = LeaveRequest.objects.get(id=pk)
    leave_req.status = 'submitted_for_approval'
    leave_req.save()

    # start business flow
    leave_req.submit_for_approval()

    msg = 'Leave Request submitted for Approval'
    messages.success(request, msg)
    return HttpResponseRedirect(
        reverse('leave-request-detail', args=[pk]))
