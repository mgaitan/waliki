.. _write_plugin:

Write a plugin
==============

Waliki has a very little core designed to be extensible with **plugins**.

At the moment, there are a few plugins built in but you can create a new one very easily.

A plugin is a normal Django app, with a file named ``waliki_plugin.py`` that defines a subclass of ``BasePlugin``.

As an example, see the `waliki.git.waliki_plugin.py`.

.. literalinclude:: ../waliki/git/waliki_plugin.py
   :language: python


What can a plugin do?
---------------------

In the first place, it's important to remark that a waliki plugin **is a django app**, so you can do with them anything an app can do: define new models, add or override templates, connect signals, etc.

.. tip:: Moreover, you can override a waliki core view! It's possible because the urls
         registered by plugins take precedence over the core ones.

In addition, you can register "actions" (views that receive a page slug as parameter).

The field ``extra_page_actions`` is a list of tuples ``('url_name', 'link text')``, where each ``url_name`` is reversed passing the page's ``slug`` as parameter. These actions appear in the dropdown of the * "Edit"* button.

Analogously, ``extra_edit_actions`` add "buttons" (links) to the editor toolbar.

Extending templates with entry points
+++++++++++++++++++++++++++++++++++++

Another thing a plugin can do is to extend the core templates. It leverages in the template tag ``entry_point``.

Wherever a tag ``{% entry_point 'name' %}`` is present, this templatetag will look for templates named ``waliki/<plugin_slug>_name`` for each plugin registered and it will include those found.


For example, the block ``{% block content %}`` in ``edit.html`` ends like this:

.. code-block:: html

        ...

        {% entry_point 'edit_content' %}
    {% endblock content %}


At that point, the template ``waliki/attachments_edit_content.html`` (and any other
template with the ``waliki/<plugin_slug>_edit_content.html``) will be appended
, using a standard include_ that receives the whole context.


.. tip:: you can `search the code <https://github.com/mgaitan/waliki/search?utf8=%E2%9C%93&q=entry_point+extension%3Ahtml>`_ to know every template entry point available


.. _include: https://docs.djangoproject.com/en/dev/ref/templates/builtins/#include

Waliki signals
++++++++++++++

In addition to the `built-in model signals <https://docs.djangoproject.com/en/dev/ref/signals/#module-django.db.models.signals>`_, your plugin can connect receivers functions to the signals that Waliki sends when few actions happen. At the moment, there is one:

* ``page_saved`` is sent just after saving a page. The parameters are the
  ``page`` instance, the ``user`` who edited the page,  and
  the optional ``message``. For example, Git extensions uses it to make a commit with the new comment.

.. note:: Of course, you can add any new signals you need!
