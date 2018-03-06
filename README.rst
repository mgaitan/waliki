
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

.. image:: https://img.shields.io/pypi/wheel/waliki.svg
    :target: https://pypi.python.org/pypi/waliki/
    :alt: Wheel Status

:home: https://github.com/mgaitan/waliki/
:demo: http://waliki.pythonanywhere.com
:documentation: http://waliki.rtfd.org
:twitter: `@Waliki_ <http://twitter.com/Waliki_>`_ // `@tin_nqn_ <http://twitter.com/tin_nqn_>`_
:group: https://groups.google.com/forum/#!forum/waliki-devs
:license: `BSD <https://github.com/mgaitan/waliki/blob/master/LICENSE>`_

At a glance, Waliki has these features:

* File based content storage.
* UI based on Bootstrap and CodeMirror
* Version control and concurrent edition for your content using `git <http://waliki.readthedocs.org/en/latest/git.html>`_
* An `extensible architecture <http://waliki.readthedocs.org/en/latest/write_a_plugin.html>`_ through plugins
* reStructuredText or Markdown support, configurable per page
  (and it's easy to add extensions)
* A very simple *per slug* `ACL system <http://waliki.readthedocs.org/en/latest/acl.html>`_
* A nice `attachments manager <http://waliki.readthedocs.org/en/latest/attachments.html>`_ (that respects the permissions over the page)
* Realtime `collaborative edition <http://waliki.readthedocs.org/en/latest/togetherjs.html>`_ via togetherJS
* Wiki content embeddable in any django template (as a "`dummy CMS <http://waliki.readthedocs.org/en/latest/boxes.html>`_")
* Few helpers to migrate content (particularly from MoinMoin, using moin2git_)
* It `works <https://travis-ci.org/mgaitan/waliki>`_ with Python 2.7, 3.4 or PyPy in Django 1.8, 1.9 (and 1.10, most probably)

It's easy to create a site powered by Waliki using the preconfigured project_ which is the same code that motorize the demo_.

Waliki was inspired in Github's wikis, but it tries to be a bit smarter than many others `git backed wiki engines`_ at handling changes: instead of a hard *"newer wins"* or *"page blocking"* approaches, Waliki uses git's merge facilities on each save. So, if there was another change during an edition and git can merge them automatically, it's done and the user is notified. If the merge fails, the last edition is still saved but the editor is reloaded asking the user to fix the conflict.

.. _project: https://github.com/mgaitan/waliki/tree/master/waliki_project
.. _demo: http://waliki.pythonanywhere.com
.. _git backed wiki engines: https://waliki.pythonanywhere.com/Git-powered-wiki-engines

Getting started
----------------

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
        'waliki.search',        # optional, additional configuration required
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

    $ python manage.py migrate


.. tip::

   Do you already have some content? Put it in your ``WALIKI_DATA_DIR`` (or set it to the actual path) and run::

        $ python manage.py sync_waliki

   Do you want everybody be able to edit your wiki? Set::

        WALIKI_ANONYMOUS_USER_PERMISSIONS = ('view_page', 'add_page', 'change_page')

   in your project's settings.



Contribute
----------

This project is looking for contributors. If you have a feature you'd like to see implemented or a bug you'd liked fixed, the best and fastest way to make that happen is to implement it and submit it back upstream for consideration. All contributions will be given thorough consideration.

Everyone interacting in the Waliki project's codebases, issue trackers and mailing lists is expected to follow the `PyPA Code of Conduct`_.


Why *Waliki* ?
----------------

**Waliki** is an `Aymara <http://en.wikipedia.org/wiki/Aymara_language>`_ word that means *all right*, *fine*.
It sounds a bit like *wiki*, has a meaningful sense and also plays with the idea of using a non-mainstream language [1]_ .

And last but most important, it's a humble tribute to the president `Evo Morales <http://en.wikipedia.org/wiki/Evo_Morales>`_ and the Bolivian people.


.. [1] *wiki* itself is a hawaiian word
.. _moin2git: https://github.com/mgaitan/moin2git
.. _`PyPA Code of Conduct`: https://www.pypa.io/en/latest/code-of-conduct/
