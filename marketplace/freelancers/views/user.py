from django.views.generic import (
    UpdateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from ..forms.user import UserForm
from django.contrib.auth import get_user_model
UserModel = get_user_model()


class UserUpdateView(
    LoginRequiredMixin,
    UpdateView
):
    model = UserModel
    form_class = UserForm
    slug_field = 'username'

    def get_success_url(self):
        return reverse_lazy(
            'freelance:joblist',
        )

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        object.save()
        return super().form_valid(form)

    def get_queryset(self):
        queryset = super(UserUpdateView, self).get_queryset()
        queryset = queryset.filter(
            id=self.request.user.id,
        )

        return queryset
