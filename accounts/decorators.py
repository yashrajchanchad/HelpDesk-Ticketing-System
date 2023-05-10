from django.shortcuts import render

from functools import wraps


def ticket_owner_required(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        if request.user and not request.user.is_it_manager and not request.user.is_it_engineer:
            return f(request, *args, **kwargs)
        render(request, 'errors/permission_error.html')
    return wrapper


def ticket_owner_or_manager_required(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        if (request.user or request.user.is_it_manager) and not request.user.is_it_engineer:
            return f(request, *args, **kwargs)
        return render(request, 'errors/permission_error.html')
    return wrapper


def it_manager_required(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        if request.user and request.user.is_it_manager:
            return f(request, *args, **kwargs)
        return render(request, 'errors/permission_error.html')
    return wrapper


def it_engineer_required(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        if request.user and request.user.is_it_engineer:
            return f(request, *args, **kwargs)
        return render(request, 'errors/permission_error.html')
    return wrapper
