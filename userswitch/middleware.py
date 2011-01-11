from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import auth
from django.http import HttpResponseRedirect

if not hasattr(settings, 'USERSWITCH_OPTIONS'):
    settings.USERSWITCH_OPTIONS = dict()

# Load defaults for missing settings
USERSWITCH_OPTIONS = {
    'css_class': settings.USERSWITCH_OPTIONS.get('css_class', 'userswitch'),
    'css_inline': settings.USERSWITCH_OPTIONS.get('css_inline', 'position:absolute;top:5px;right:5px;z-index:999;'),
    'content_types': settings.USERSWITCH_OPTIONS.get('content_types', ('text/html', 'application/xhtml+xml')),
    'auth_backend': settings.USERSWITCH_OPTIONS.get('auth_backend', 'django.contrib.auth.backends.ModelBackend'),
    'users': settings.USERSWITCH_OPTIONS.get('users', tuple()),
}


# HTML for the widget
USERSWITCH_WIDGET = """
<div class="%(css_class)s" style="%(css_inline)s">
  <select onChange="var username = options[selectedIndex].value; document.location.href = '/?userswitch_username='+username">
    <options>
  </select>
</div>
""" % USERSWITCH_OPTIONS


class UserSwitchMiddleware(object):
    """
    Appends user switcher widget just before the </body> tag in the response html
    """
    def process_request(self, request):
        """
        Logout current user and login the user specified in the username.
        """

        #Check if a user switch was requested by using a GET argument. If not, proceed to normal view.
        username = request.GET.get('userswitch_username',None)
        if username:
            user = User.objects.get(username=username)
            # If the requested user in not found then this throws an expcetion.
            # It is not a bug, it is intentional. If the user does not exist in the DB,
            # it is a good idea to show that than to have the developer wondering why
            # the user is not switching.
            user = User.objects.get(username=username)

            # user.backend is needed for the the auth.login to work properly
            user.backend = USERSWITCH_OPTIONS['auth_backend']

            auth.logout(request)
            auth.login(request,user)

            # Redirect to the refering URL, if there is one
            if request.META.has_key('HTTP_REFERER'):
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                return HttpResponseRedirect('/')

        return None     

    def process_response(self, request, response):
        if settings.DEBUG and response.status_code == 200:
            if response['Content-Type'].split(';')[0].strip() in USERSWITCH_OPTIONS['content_types']:
                content = response.content
                content = content.replace('</body>','USERSWITCH_HTML</body>')
                options_html = '<option value="0">Switch User</option>'

                if USERSWITCH_OPTIONS['users']:
                    users = USERSWITCH_OPTIONS['users']
                else:
                    users = User.objects.all()

                for user in users:
                    options_html += '<option value="%s">%s</option>' % (user, user)

                switch_widget = USERSWITCH_WIDGET.replace('<options>',options_html)

                response.content = content.replace('</body>','%s</body>' % switch_widget)

        return response
