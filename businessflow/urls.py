from django.conf.urls import url, patterns

from businessflow.views import(
    TaskListView,
    TaskDetailView
)

urlpatterns = patterns(
    'businessflow.views',

    url(r'^tasks/$',
        TaskListView.as_view(),
        name='businessflow-task-list'),

    url(r'^tasks/(?P<pk>\d+)/$',
        TaskDetailView.as_view(),
        name='businessflow-task-detail'),

)
