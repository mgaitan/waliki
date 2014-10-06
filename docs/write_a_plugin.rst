.. _write_plugin:

Write a plugin
==============

Waliki has a very little core designed to be extensible with **plugins**.

At the moment, there are only two extensions available (`Git </git>`_ and `rst2pdf </get-as-pdf>`_) but you can create a new one very easily.

A plugin is a normal Django app, with a file named ``waliki_plugin.py`` with a subclass of ``BasePlugin``.

As an example, see the `waliki.git.waliki_plugin.py`.

.. literalinclude:: ../waliki/git/waliki_plugin.py
   :language: python


The field ``extra_page_actions`` is a list ``('url_name', 'link text')`` tuples, where each ``url_name`` is reversed passing the page's `slug` as parameters. This actions appear in the dropdown of the * "Edit"* button.


What a plugin could do?
------------------------

Everything you can do with and app: add views, add or override templates, etc.

For connect receivers functions to the signals that Waliki sends when few actions happen. At the moment there is one:

* ``page_saved`` is sent just after save a page. The parameters are the
  ``page`` instance, the ``user`` who edited the page,  and
  the optional ``message``. For example, Git extensions uses it to make a commit with the new comment.

.. note:: Of course, you can add any new signal you need!
