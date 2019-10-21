from django.urls import path
from .views import (
    views,
    job,
    user
)

app_name = 'freelancer'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('jobs/', job.JobListView.as_view(), name='joblist'),
    path('job/create/', job.JobCreateView.as_view(), name='jobcreate'),
    path('job/<slug:slug>/', job.JobDetailView.as_view(), name='jobdetail')
]


# users views
urlpatterns += [
    path('accounts/update/<slug:slug>/',
         user.UserUpdateView.as_view(), name='userupdate'),
    path('job/accept/<slug:code>/', job.JobAcceptedRedirectView.as_view(),
         name='acceptjob'),
    path('jobs/accepted/', job.AcceptedJobListView.as_view(),
         name='acceptedjoblist'),
]
