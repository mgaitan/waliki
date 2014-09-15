
**Waliki** is an extensible wiki app for Django with a Git backend.


.. image:: https://badge.fury.io/py/waliki.png
    :target: https://badge.fury.io/py/waliki

..

    .. image:: https://travis-ci.org/mgaitan/waliki.png?branch=master
        :target: https://travis-ci.org/mgaitan/django-waliki

    .. image:: https://coveralls.io/repos/mgaitan/waliki/badge.png?branch=master
        :target: https://coveralls.io/r/mgaitan/waliki?branch=master

.. image:: https://readthedocs.org/projects/waliki/badge/?version=latest
   :target: https://readthedocs.org/projects/waliki/?badge=latest
   :alt: Documentation Status


:home: https://github.com/mgaitan/waliki/
:documentation: http://waliki.rtfd.org (under development)
:group: https://groups.google.com/forum/#!forum/waliki-devs
:license: `BSD <https://github.com/mgaitan/waliki/blob/master/LICENSE>`_

.. :demo: http://waliki.nqnwebs.com


At a glance, Waliki has:

- File based content storage.
- Version control for your content using Git
- Extensible architecture with plugins
- Markdown, reStructuredText or textile markups. Easy to add more.
- UI based on Twitter's Bootstrap

How to start
------------

Install with::

    $ pip install waliki

Add ``waliki`` and optionals plugins to your INSTALLED_APPS::

    INSTALLED_APPS = (
        ...
        'waliki',
        'waliki.git'   # optional
        ...
    )

Include the waliki urls in you project's ``urls.py``::

    urlpatterns = patterns('',
        ...
        url(r'^wiki/', include('waliki.urls')),
        ...
    )

Enjoy!


Why "Waliki" ?
----------------

**Waliki** is an `Aymara <http://en.wikipedia.org/wiki/Aymara_language>`_ word that means *all right*, *fine*.

It sounds a bit like *Wiki*, has a meaningful sense for this project
and also plays with the idea of using a "non mainstream" language [1]_ .

And last but not less important, it's a humble tribute to bolivian `President Evo Morales Ayma <http://en.wikipedia.org/wiki/Evo_Morales>`_

.. [1] *wiki* itself is a hawaiian word