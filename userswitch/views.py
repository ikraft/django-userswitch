from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.conf import settings


def switch(request, username):
    """
    Logout current user and login the user specified in the username.
    """

    # If the requested user in not found then this throws an expcetion.
    # It is not a bug, it is intentional. If the user does not exist in the DB,
    # it is a good idea to show that than to have the developer wondering why
    # the user is not switching.
    user = User.objects.get(username=username)

    # user.backend is needed for the the auth.login to work properly
    user.backend = settings.USERSWITCH_OPTIONS.get('auth_backend', 'django.contrib.auth.backends.ModelBackend')

    auth.logout(request)
    auth.login(request,user)

    # Redirect to the refering URL, if there is one
    if request.META.has_key('HTTP_REFERER'):
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    else:
        return HttpResponseRedirect('/')
