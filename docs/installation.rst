============
Installation
============

Install via pip
---------------

To install the latest stable release, run::

    $ pip install waliki

By default Waliki use reStructuredText as its markup, so docutils and other required dependencies are retrieved. If you prefer a Markdown only wiki, install it as following::

    $ pip install waliki[markdown]

Alternatively, if you want install every dependency, use::

    $ pip install waliki[all]


Configure ``settings.INSTALLED_APPS``
-------------------------------------


Add ``waliki`` and optionals plugins to your INSTALLED_APPS::

    INSTALLED_APPS = (
        ...
        'waliki',
        'waliki.git'   # optional
        ...
    )

.. attention::

    To enable ``waliki.git`` you need Git installed in your system. In Debian/Ubuntu::

        $ sudo apt-get install git

Sync database
-------------

Although Waliki stores page content as flat files, it uses a model
to store page titles, slugs and other fields.

Create this model table using::

    $ python manage.py syncdb

Include url patterns
--------------------

Include the waliki urls in you project's ``urls.py``. For example::

    urlpatterns = patterns('',
        ...
        url(r'^wiki/', include('waliki.urls')),
        ...
    )

Waliki will handle the inclusion of installed plugins urls automatically.




