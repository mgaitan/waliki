
Extension "Get as PDF"
=======================

This a very simple plugin that leverage on rst2pdf_ to get a PDF version of a page.

.. note::

   The code is at https://github.com/mgaitan/waliki/blob/master/extensions/rst2pdf.py

It just register a new `action view`_ in the dropdown menu as *"Get as PDF"*. For obvious reasons, it requires set ``MARKUP = 'restructuredtext'`` and install rst2pdf in your virtualenv or system wide.

.. tip:: Should be trivial to write new extensions that
         add support to other converters tools like any ``rst2*``
         or Pandoc_ to convert from markdown.

Active it appending ``'rst2pdf'`` to the ``EXTENSIONS`` list. For example, this wiki has::

   # encoding: utf-8
   SECRET_KEY= 'my_very_hashy_key'
   TITLE = 'Waliki Demo'
   PRIVATE = False
   MARKUP = 'restructuredtext'
   EXTENSIONS = ['Git', 'rst2pdf']

.. _Pandoc:
.. _rst2pdf: http://rst2pdf.ralsina.com.ar