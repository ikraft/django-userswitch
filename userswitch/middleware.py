from django.conf import settings
from django.contrib.auth.models import User

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
  <select onChange="var id = options[selectedIndex].value; document.location.href = '/userswitch/'+id">
    <options>
  </select>
</div>
""" % USERSWITCH_OPTIONS


class UserSwitchMiddleware(object):
    """
    Appends user switcher widget just before the </body> tag in the response html
    """

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
