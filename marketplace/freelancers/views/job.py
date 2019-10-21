from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from ..models import (
    Job,
    Accept
)
from ..forms.job import JobForm
from ..decorators import user_name
from datetime import date


class JobListView(
    LoginRequiredMixin,
    ListView
):

    model = Job
    paginate_by = 20

    def get_queryset(self):
        queryset = super(JobListView, self).get_queryset()
        queryset = queryset.filter(
            expired__gte=date.today(),
            concluded=False
        )

        return queryset


class JobCreateView(
    LoginRequiredMixin,
    CreateView
):
    model = Job
    form_class = JobForm

    @user_name
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy(
            'freelance:joblist',
        )

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.save()
        return super().form_valid(form)


class JobDetailView(
    LoginRequiredMixin,
    DetailView
):
    model = Job
    slug_field = 'code'

    @user_name
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class JobAcceptedRedirectView(
    LoginRequiredMixin,
    RedirectView
):

    permanent = False
    query_string = False
    # pattern_name = 'acceptedjoblist'
    url = reverse_lazy('freelance:acceptedjoblist')

    def get_redirect_url(self, *args, **kwargs):
        job = get_object_or_404(
            Job,
            code=kwargs['code'],
            expired__gte=date.today(),
            concluded=False
        )

        if job.available:
            obj, created = Accept.objects.update_or_create(
                job=job,
                user=self.request.user,
            )
        else:
            messages.warning(self.request, 'The job cannot be assigned.')

        return super().get_redirect_url(*args, **kwargs)


class AcceptedJobListView(
    LoginRequiredMixin,
    ListView
):
    model = Job
    paginate_by = 20

    def get_queryset(self):
        queryset = super(AcceptedJobListView, self).get_queryset()
        queryset = queryset.filter(
            accept__user=self.request.user,
            accept__reject=False
        )

        return queryset
