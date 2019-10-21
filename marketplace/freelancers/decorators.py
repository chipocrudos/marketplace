from django.urls import reverse_lazy
from functools import wraps
from django.http import HttpResponseRedirect


def user_name(view_func):
    def get_profile_url(user):
        return reverse_lazy(
            'freelance:userupdate',
            args=(
                user.username,
            )
        )

    @wraps(view_func)
    def _wrapped_view(self, request, *args, **kwargs):

        if not request.user.first_name and not request.user.last_name:
            return HttpResponseRedirect(
                get_profile_url(request.user)
            )

        return view_func(self, request, *args, **kwargs)

    return _wrapped_view
