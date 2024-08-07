from django.contrib.auth.decorators import login_required as original_login_required
from django.contrib import messages
from django.shortcuts import redirect

def login_required(function=None, redirect_field_name='next', login_url=None):
    def decorator(view_func):
        @original_login_required(login_url=login_url, redirect_field_name=redirect_field_name)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.info(request, 'You need to log in to access this page.')
            return view_func(request, *args, **kwargs)
        return _wrapped_view

    if function:
        return decorator(function)
    return decorator
