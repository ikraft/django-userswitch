from django.conf.urls.defaults import *


urlpatterns = patterns('userswitch.views',
    url(r'^(?P<username>.+)$', 'switch', name='userswitch_switch'),
)

