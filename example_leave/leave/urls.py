from django.conf.urls import url, patterns

from leave.views import(
    LeaveRequestListView,
    LeaveRequestCreateView,
    LeaveRequestDetailView,
)

urlpatterns = patterns('leave.views',
    url(r'^requests/$',
        LeaveRequestListView.as_view(),
        name='leave-request-list'),
    url(r'^requests/create/$',
        LeaveRequestCreateView.as_view(),
        name='leave-request-create'),
    url(r'^requests/(?P<pk>\d+)/$',
        LeaveRequestDetailView.as_view(),
        name='leave-request-detail'),

    url(r'^requests/(?P<pk>\d+)/approval_submit/$',
        'approval_submit',
        name='leave-request-approval-submit'),

)
