.. _pdf:

Plugin "Get as PDF"
=======================

This a very simple plugin that leverages on rst2pdf_ to get a PDF version of a page.

It registers a new :ref:`extra_page_action view <write_plugin>` in the dropdown menu as *"Get as PDF"*. For obvious reasons, it only appears in reStructuredText pages.

Get it working on python 3
--------------------------

rst2pdf_ is a python2 software, so if we are running Waliki with python3 is not possible to run rst2pdf inside the virtualenv.
To get it working you simply have to install rst2pdf as an OS package (apt-get install rst2pdf or pacman -S python2-rst2pdf) and then add 
`WALIKI_PDF_RST2PDF_BIN` to your waliki settings file detailing the rst2pdf binary path. For example::

    WALIKI_PDF_RST2PDF_BIN='/usr/bin/rst2pdf'


.. tip:: It should be trivial to write new plugins that
         add support to other converter tools like any ``rst2*``
         or Pandoc_ to convert from markdown.

.. _rst2pdf: https://pypi.python.org/pypi/rst2pdf
.. _pandoc: http://johnmacfarlane.net/pandoc/
