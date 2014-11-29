=================
The "Git" backend
=================

The Git backend is a simple plugin but, probably, it adds the most interesting features to Waliki.

Basically, ``waliki.git`` converts your content folder in a git repository, and makes a commit on each edition.

With this simple logic you'll get:

* History of changes (who, when, what)
* Diff: compare any version an see what was added or removed
* Smart concurrent edition handling: don't lock editions, merge them!
* View and restore old revisions (without lose history)
* Simple stats: how many lines were added or removed. (go to the history page to see it in action!)
* Backup (pushing your repo to a remote place)
* Edit your content outside the web using the editor of your preference!
* Webhook/s (pull changes from a remote repository)


To install it add ``'waliki.git'`` after ``'waliki'`` in your ``settings.INSTALLED_APPS``.

.. tip:: This plugin is optional, but strongly recommended.


This extension uses the ``git`` command line machinary wrapped via the wonderful `sh <https://amoffat.github.com/sh>`_ package. Although it could have a performance impact compared with a python git library, my experience is that `pygit2 <http://www.pygit2.org>`_ is a bit complex to use and `GitPython <https://github.com/gitpython-developers/GitPython>`_ doesn't work with Python 3.

The *pull* webhook
------------------

``waliki.git`` has a webhook endpoint that receives an HTTP POST requests (without parameters) to pull and sync content from a remote repository::

    POST http://yoursite.com[/<waliki_prefix>]/hooks/pull/<remote>


This is useful to sync your wiki whenever a repository is pushed to. For example when you push `to github <https://developer.github.com/webhooks/>`_.