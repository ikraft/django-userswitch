from distutils.core import setup

setup(
    name = "django-userswitch",
    version = "0.1",
    packages = ['userswitch',],
    license = "New BSD License",
    author = "iKraft Software (P) LTD.",
    author_email = "hello@ikraftsoft.com",
    maintainer = "iKraft Software (P) LTD.",
    maintainer_email = "hello@ikraftsoft.com",
    description = "A quick 'n' dirty Django app for switching between different users while testing",
    long_description=open('README.rst').read(),
    url = "https://github.com/ikraftsoft/django-userswitch",
    download_url="https://github.com/ikraftsoft/django-userswitch/tarball/master",
    install_requires=[
        'Django>=1.2',
    ],
    include_package_data=True,
)
