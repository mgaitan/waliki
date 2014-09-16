Plugin "Get as PDF"
=======================

This a very simple plugin that leverage on rst2pdf_ to get a PDF version of a page.

It registers a new :ref:`extra_page_action view <write_plugin>` in the dropdown menu as *"Get as PDF"*. For obvious reasons, it only appear in reStructuredText pages.

.. tip:: Should be trivial to write new plugins that
         add support to other converters tools like any ``rst2*``
         or Pandoc_ to convert from markdown.

.. _rst2pdf: https://pypi.python.org/pypi/rst2pdf