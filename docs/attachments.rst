.. _attachments:
Plugin "Attachments"
=======================

This plugin allows to upload files to a page and include it in the text as an embedded image or a link.

Using the standard template, it extends the ``edit`` page with a new button 'Attachments'

On old-fashion browsers without FormData_ support (i.e. Internet Explorer < 10) the ajaxified upload form (including the uploading progress bar) degrades to a popup window.


.. _FormData: https://developer.mozilla.org/en-US/docs/Web/API/FormData

Setup
-------

It requires `django-sendfile`_ as an extra requirement. Install it via pip::

    $ pip install django-sendfile

then adds ``waliki.attachments`` and ``sendfile`` to your ``INSTALLED_APPS``:

   INSTALLED_APPS = (
        ...
        'waliki',
        'waliki.attachments',
        ...
        'sendfile',
        ...
    )


.. _django-sendfile: https://github.com/johnsensible/django-sendfile


Lastly, configure ``sendfile``. This package allows serve the attached files using your web server, but still checking the permission.


.. tip:: to view/download an attachment, the user needs the 'view_page' permission
         over the current slug

For a basic configuration set::


    SENDFILE_BACKEND = 'sendfile.backends.simple'


.. attention:: by default, Waliki uploads attachments to the path /waliki_attachments/<page_slug>/<filename>. Override the function ``WALIKI_UPLOAD_TO`` in your settings if you need another structure.





Read the django-sendfile's documentation for specific instructions if you use Nginx or Apache.


