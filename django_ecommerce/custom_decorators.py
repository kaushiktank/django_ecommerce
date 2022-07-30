from django.shortcuts import redirect

def user_not_logged_in(request, redirect_url=None):
    def wrapper(request, *args, **kw):
        if request.user.is_authenticated:
            return redirect(redirect_url)

    return wrapper
