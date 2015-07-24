.. _rest:

=========
REST API
=========
The ``waliki.rest`` plugin together ``waliki.git`` provides a set of REST API endpoints.

With this plugin you'll get:

URLs
----

| List all Pages
| ``GET http://yoursite.com[/<waliki_prefix>]/<WALIKI_API_ROOT>/all``
|
| Add Page
| ``POST http://yoursite.com[/<waliki_prefix>]/<WALIKI_API_ROOT>/new``
|
| Retrieve Page
| ``GET http://yoursite.com[/<waliki_prefix>]/<WALIKI_API_ROOT>/<slug>``
|
| Edit Page
| ``POST http://yoursite.com[/<waliki_prefix>]/<WALIKI_API_ROOT>/<slug>/edit``
|
| Move Page
| ``POST http://yoursite.com[/<waliki_prefix>]/<WALIKI_API_ROOT>/<slug>/move``
|
| Delete Page
| ``POST http://yoursite.com[/<waliki_prefix>]/<WALIKI_API_ROOT>/<slug>/delete``
|
| History of changes
| ``GET http://yoursite.com[/<waliki_prefix>]/<WALIKI_API_ROOT>/<slug>/history``
|
| Retrieve a version
| ``GET http://yoursite.com[/<waliki_prefix>]/<WALIKI_API_ROOT>/<slug>/version/<version>/``
|
| Diff
| ``GET http://yoursite.com[/<waliki_prefix>]/<WALIKI_API_ROOT>/<slug>/diff/<new_version>..<old_version>``

Setup
-------

It requires `djangorestframework`_ as requirement. Install it via pip::

    $ pip install djangorestframework

To install it, add ``'waliki.rest'`` and ``'rest_framework'`` after ``'waliki.git'`` in your ``settings.INSTALLED_APPS``::

   INSTALLED_APPS = (
        ...
        'waliki',
        ...
        'waliki.git',
        'waliki.rest',
        ...
        'rest_framework',
        ...
    )

| Default url for restful service:

``WALIKI_API_ROOT = 'API'``

.. _djangorestframework: https://github.com/tomchristie/django-rest-framework
