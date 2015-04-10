
**Waliki** is an extensible wiki app for Django with a Git backend.


.. attention:: It's in an early development stage. I'll appreciate your feedback and help.


.. image:: https://badge.fury.io/py/waliki.png
    :target: https://badge.fury.io/py/waliki

.. image:: https://travis-ci.org/mgaitan/waliki.png?branch=master
    :target: https://travis-ci.org/mgaitan/waliki

.. image:: https://coveralls.io/repos/mgaitan/waliki/badge.png?branch=master
    :target: https://coveralls.io/r/mgaitan/waliki?branch=master

.. image:: https://readthedocs.org/projects/waliki/badge/?version=latest
   :target: https://readthedocs.org/projects/waliki/?badge=latest
   :alt: Documentation Status

.. image:: https://pypip.in/wheel/waliki/badge.svg
    :target: https://pypi.python.org/pypi/waliki/
    :alt: Wheel Status

:home: https://github.com/mgaitan/waliki/
:demo: http://waliki.pythonanywhere.com
:documentation: http://waliki.rtfd.org
:twitter: `@Waliki_ <http://twitter.com/Waliki_>`_ // `@tin_nqn_ <http://twitter.com/tin_nqn_>`_
:group: https://groups.google.com/forum/#!forum/waliki-devs
:license: `BSD <https://github.com/mgaitan/waliki/blob/master/LICENSE>`_

At a glance, Waliki has this features:

* File based content storage.
* UI based on Bootstrap and CodeMirror
* Version control and concurrent edition for your content using git
* An extensible architecture with plugins
* reStructuredText or Markdown support, configurable per page
  (and it's easy to add extensions)
* A very simple *per slug* ACL system
* A nice page attachments manager (that respects the page permissions)
* Realtime collaborative edition via togetherJS
* Wiki content embeddable in any django template (as a "dummy CMS")
* Few helpers to migrate content (particularly from MoinMoin, using moin2git_)
* It works with Python 2.7, 3.3, 3.4 or PyPy in Django 1.6 or newer

How to start
------------

Install it with pip::

    $ pip install waliki[all]

Or the development version::

    $ pip install https://github.com/mgaitan/waliki/tarball/master


Add ``waliki`` and the optionals plugins to your INSTALLED_APPS::

    INSTALLED_APPS = (
        ...
        'waliki',
        'waliki.git',           # optional but recommended
        'waliki.attachments',   # optional but recommended
        'waliki.pdf',           # optional
        'waliki.slides',        # optional
        'waliki.togetherjs',    # optional
        ...
    )

Include ``waliki.urls`` in your project's ``urls.py``. For example::

    urlpatterns = patterns('',
        ...
        url(r'^wiki/', include('waliki.urls')),
        ...
    )

Sync your database::

    $ python manage.py migrate   # syncdb in django < 1.7



.. tip::

   Do you already have some content? Put it in your ``WALIKI_DATA_DIR`` (or set it to the actual path) and run::

        $ python manage.py sync_waliki

   Do you want everybody be able to edit your wiki? Set::

        WALIKI_ANONYMOUS_USER_PERMISSIONS = ('view_page', 'add_page', 'change_page')

   in your project's settings.


Why *Waliki* ?
----------------

**Waliki** is an `Aymara <http://en.wikipedia.org/wiki/Aymara_language>`_ word that means *all right*, *fine*.

It sounds a bit like *wiki*, has a meaningful sense and also plays with the idea of using a non-mainstream language [1]_ .

And last but most important, it's a humble tribute to the president `Evo Morales <http://en.wikipedia.org/wiki/Evo_Morales>`_ and the Bolivian people.

.. [1] *wiki* itself is a hawaiian word
.. _moin2git: https://github.com/mgaitan/moin2git