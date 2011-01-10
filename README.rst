Django UserSwitch
=================
A quick 'n' dirty Django app for switching between different users while testing

Installation
-------------

To install the latest version:: 

    pip git+git://git://github.com/ikraftsoft/django-userswitch#egg=django-userswitch

It can also be installed from PyPI with ``pip`` or ``easy_install``::

    pip install django-userswitch


    easy_install install django-userswitch

Setup & Usage
--------------

Step 1: Add ``userswitch`` middleware to the ``MIDDLEWARE_CLASSES`` in settings.py
  after the default middlewares::

  	MIDDLEWARE_CLASSES = (
	    'django.middleware.common.CommonMiddleware',
	    'django.contrib.sessions.middleware.SessionMiddleware',
	    'django.middleware.csrf.CsrfViewMiddleware',
	    'django.contrib.auth.middleware.AuthenticationMiddleware',
	    'django.contrib.messages.middleware.MessageMiddleware',
	    ...
	    'userswitch.middleware.UserSwitchMiddleware',
	)

Step 2: Add the following line to your root ``url.py``::

        from django.conf import settings
	....

	if settings.DEBUG:
	    urlpatterns += pattern('',
	        (r'^userswitch/', include('userswitch.urls'))
	    )


Step 3: Optionally you can add ``USERSWITCH_OPTIONS`` dict to the settings.py::
    
        USERSWITCH_OPTIONS = {
            'css_class': '',       # CSS class to be added to the switcher widget. Default='userswitch'.
            'css_inline': '',     # Inline css for the switcher widget, if any
            'content_types': (),   # a tuple of content-type for which to render switcher widget. Default = ('text/html', 'application/xhtml+xml')
            'auth_backend': '',   # Custom auth backend if any. Default = 'django.contrib.auth.backends.ModelBackend'
            'users': (),           # List of usernames(as strings) to be shown in the switcher widget. If its empty, all users are loaded.
        }

Note: default value of ``css_inline`` option provides some basic absolute 
positioning. To change those either specify ``css_inline`` option
manually or override ``position``, ``top``, ``right`` in the class
specified in ``css_class`` with ``!important``.
    

That's All!
