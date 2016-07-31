from django.conf.urls import url, patterns

from simpleflow.views import(
    TaskListView,
    TaskDetailView
)

urlpatterns = patterns(
    'simpleflow.views',

    url(r'^tasks/$',
        TaskListView.as_view(),
        name='simpleflow-task-list'),

    url(r'^tasks/(?P<pk>\d+)/$',
        TaskDetailView.as_view(),
        name='simpleflow-task-detail'),

)
