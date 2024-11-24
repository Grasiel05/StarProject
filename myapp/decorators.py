from django.shortcuts import render

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, '403.html', status=403)
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
