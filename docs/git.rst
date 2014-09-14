=================
The "Git" plugin
=================

The ``Git`` plugin converts your content folder in a git repository, and make a commit on each edition.

With this simple logic you'll get:

* History of changes (who, when, what)
* Diff: compare any version an see what was added or removed
* See an old version of a page and restore it if you want (without loose history)
* Fancy relative dhatetimes out of the box
* Simple stats: how many lines were added or removed. (go to the history page to see it in action!)
* Backup (pushing your repo to a remote place)
* Edit your content outside the web using the editor you prefer!

Also would be possible:

- Alert about conflicts (concurrent edition),
- merge versions
- more ideas?

.. tip:: This plugin is optional, but strongly recommended.

To install it add ``'waliki.git'`` after ``'waliki'`` in you ``settings.INSTALLED_APPS``.

This extension uses the ``git`` command line machinary wrapped via the wonderful `sh <https://amoffat.github.com/sh>`_ package. Although it could have a performance impact compared with a python git library, my experience is that `pygit2 <http://www.pygit2.org>`_ is a bit complex to use and `GitPython <https://github.com/gitpython-developers/GitPython>`_ doesn't work with Python 3.


