Autolinks
=========

One of the most important feature in any wiki system is the simplicity to create and link pages. Waliki has a simple support for internal links

Autolinks in reStructuredText
-----------------------------

There is autolinking support for restructuredtext with a very simple trick: if you don't explicitly define the target in a link (a word ending with and undercore like ``this_``), it will automatically point to an internal wiki page (even if it doesn't exist yet).

So, just define ``somewhere_`` and to link the page with the slug *somewhere*

How it is implemented?
++++++++++++++++++++++

It's dirty but very simple: just render the page as usual using docutils and every unreferenced target is parsed and appended to internals urls.


Autolinks in Markdown
---------------------

Waliki enables the Markdown's `WikiLinks <https://pythonhosted.org/Markdown/extensions/wikilinks.html>`_ extension by default.

Uses ``[[Somewhere]]`` to link the page with slug *somewhere*.


