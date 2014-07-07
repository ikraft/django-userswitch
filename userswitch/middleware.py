from django.conf import settings
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.core.exceptions import MiddlewareNotUsed
from django import VERSION


if VERSION[0] < 1 or (VERSION[0] == 1 and VERSION[1] < 5):
    from django.contrib.auth.models import User
else:
    from django.contrib.auth import get_user_model
    User = get_user_model()


class UserSwitchMiddleware(object):
    def __init__(self):

        if not hasattr(settings, 'USERSWITCH_OPTIONS'):
            settings.USERSWITCH_OPTIONS = dict()

        if settings.USERSWITCH_OPTIONS.get('force_on',False):
            pass
        elif getattr(settings, "DEMO_MODE", False) or not settings.DEBUG:
            raise MiddlewareNotUsed

        # Load defaults for missing settings
        self.USERSWITCH_OPTIONS = {
            'css_class': settings.USERSWITCH_OPTIONS.get('css_class', 'userswitch'),
            'css_inline': settings.USERSWITCH_OPTIONS.get('css_inline', 'position:absolute;top:5px;right:5px;z-index:16777271;'),
            'content_types': settings.USERSWITCH_OPTIONS.get('content_types', ('text/html', 'application/xhtml+xml')),
            'auth_backend': settings.USERSWITCH_OPTIONS.get('auth_backend', 'django.contrib.auth.backends.ModelBackend'),
            'replace_text': settings.USERSWITCH_OPTIONS.get('replace_text', ''),
            'users': settings.USERSWITCH_OPTIONS.get('users', tuple()),
        }

        # HTML for the widget
        self.USERSWITCH_WIDGET = """
        <div class="%(css_class)s" style="%(css_inline)s">
        <select onChange="var username = options[selectedIndex].value; document.location.href = '/?userswitch_username=' + encodeURIComponent(username);">
            <options>
        </select>
        </div>
        """ % self.USERSWITCH_OPTIONS


    def process_request(self, request):
        """
        Logout current user and login the user specified in the username.
        """
        #Check if a user switch was requested by using a GET argument. If not, proceed to normal view.
        username = request.GET.get('userswitch_username',None)
        if username:
            # If the requested user in not found then this throws an expcetion.
            # It is not a bug, it is intentional. If the user does not exist in the DB,
            # it is a good idea to show that than to have the developer wondering why
            # the user is not switching.
            user = User.objects.get(username=username)

            # user.backend is needed for the the auth.login to work properly
            user.backend = self.USERSWITCH_OPTIONS['auth_backend']

            auth.logout(request)
            auth.login(request,user)

            # Redirect to the refering URL, if there is one
            if request.META.has_key('HTTP_REFERER'):
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
            else:
                return HttpResponseRedirect('/')



    def process_response(self, request, response):
        """
        Appends user switcher widget just before the </body> tag in the response html
        """
        if response.status_code == 200 and response['Content-Type'].split(';')[0].strip() in self.USERSWITCH_OPTIONS['content_types']:

                options_html = '<option value="0">Switch User</option>'

                if self.USERSWITCH_OPTIONS['users']:
                    users = self.USERSWITCH_OPTIONS['users']
                else:
                    users = User.objects.all()

                for user in users:
                    options_html += '<option value="%s">%s</option>' % (user, user)

                switch_widget = self.USERSWITCH_WIDGET.replace('<options>',options_html)
                if self.USERSWITCH_OPTIONS['replace_text']:
                    response.content = response.content.replace(self.USERSWITCH_OPTIONS['replace_text'], switch_widget)
                else:
                    response.content = response.content.replace('</body>','%s</body>' % switch_widget)

        return response
