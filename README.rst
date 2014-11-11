
**Waliki** is an extensible wiki app for Django with a Git backend.


.. attention:: It's usable but in an early development stage. I'll appreciate your feedback and help.


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
:group: https://groups.google.com/forum/#!forum/waliki-devs
:license: `BSD <https://github.com/mgaitan/waliki/blob/master/LICENSE>`_


At a glance, Waliki has this features:

- File based content storage.
- Version control and concurrent edition for your content using Git
- Extensible architecture with plugins
- Markdown or reStructuredText. Easy to add more.
- A simple ACL system
- Attachments
- UI based on Twitter's Bootstrap and Codemirror.
- Works with Python 2.7, 3.3+ or PyPy in Django 1.5 or newer

How to start
------------

Install it with pip::

    $ pip install waliki

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
        ...
    )

Include ``waliki.urls`` in your project's ``urls.py``. For example::

    urlpatterns = patterns('',
        ...
        url(r'^wiki/', include('waliki.urls')),
        ...
    )

Sync your db::

    $ python manage.py syncdb


Enjoy!


Why "Waliki" ?
----------------

**Waliki** is an `Aymara <http://en.wikipedia.org/wiki/Aymara_language>`_ word that means *all right*, *fine*.

It sounds a bit like *wiki*, has a meaningful sense for this project
and also plays with the idea of using a non-mainstream language [1]_ .

And last but most important, it's a humble tribute to the bolivian president `Evo Morales <http://en.wikipedia.org/wiki/Evo_Morales>`_.

.. [1] *wiki* itself is a hawaiian word
