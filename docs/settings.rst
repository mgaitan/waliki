========
Settings
========

Waliki follows a `convention over configuration <http://en.wikipedia.org/wiki/Convention_over_configuration>`_
paradigm, defining sensible defaults for every constant.

You can override any settings in your project's :file:`settings.py` file


.. confval:: WALIKI_DATA_DIR

    Waliki's content path. By default it's ``<project_root>/waliki_data``

    You can set it to an absolute path. Ensure the path exists and it's writable from
    your web server

.. confval:: WALIKI_INDEX_SLUG

   The slug of the index page. Default is ``home``


.. confval:: WALIKI_ANONYMOUS_USER_PERMISSIONS

    The tuple of permissions given to not authenticated users. Default is ``('view_page',)``
    Check :ref:`acl` for further details. If there is no ``change_page`` permission,
    the anonymous user is redirected to the login page when try to edit the page.

.. confval:: WALIKI_LOGGED_USER_PERMISSIONS

    The tuple of permissions given to any authenticated user. Default is ``('view_page', 'add_page', 'change_page')``. Check :ref:`acl` for further details.



.. confval:: WALIKI_AVAILABLE_MARKUPS

    A list tha define the enabled markups. Default is ``['reStructuredText', 'Markdown']``.
    Available markups are ``reStructuredText``, ``Markdown`` and ``Textile``

.. confval:: WALIKI_DEFAULT_MARKUP

    The default markup for new pages. Default ``WALIKI_AVAILABLE_MARKUPS[0]``

.. confval:: WALIKI_SLUG_PATTERN

    Pattern used in urls to match any page related view, wich is also de filename of
    the file that store the page content. Default is ``'[a-zA-Z0-9-_\/]+'``.


.. confval:: WALIKI_SLUGIFY_FUNCTION

    String pointing to a callable that receive a text and return and slug.
    Default ``'waliki.utils.get_slug'``

    If you override it, ensure that ``your_get_slug(any_valid_slug) == any_valid_slug``


.. confval:: WALIKI_SANITIZE_FUNCTION

    .. versionadded:: 0.6

    String pointing to a callable that receive html and return and return a sanitized version of it.
    Default ``'waliki.utils.sanitize'``, which just removes ``<script>`` tags.

    You can define a more sofisticated version using `bleach <http://bleach.readthedocs.org>`_ or
    lxml's `Cleaner <http://lxml.de/api/lxml.html.clean.Cleaner-class.html>`_


.. confval:: WALIKI_MARKUPS_SETTINGS

    Dictionary of keywords arguments to extend or override the ones passed for each markup class.
    By default, this is the dictionary used

    .. code-block:: python

        {'reStructuredText': {
            # check http://docutils.sourceforge.net/docs/user/config.html
            'settings_overrides': {
                'initial_header_level': 2,
                'record_dependencies': True,
                'stylesheet_path': None,
                'link_stylesheet': True,
                'syntax_highlight': 'short',
                'halt_level': 5,
            },
            'writer': HTML5Writer(),
            'writer_name': 'html5',
            },
        'Markdown': {
                'extensions': ['wikilinks', 'headerid'],
                'extension_configs': {
                    'wikilinks': {'build_url': get_url},
                    'headerid': {'level': 2},
                }
            }
        }


.. confval:: WALIKI_BREADCRUMBS

    .. versionadded:: 0.6

    If ``True``, show a breadcrumbs with links to "parent" pages. Default is ``False``


.. confval:: WALIKI_PDF_INCLUDE_TITLE

    Apply if :ref:`PDF plugin <pdf>` is installed.

    As the title is not part of the file content but stored in the database, it should be given
    to rst2pdf. Default is ``False``

.. confval:: WALIKI_PDF_RST2PDF_BIN

    Apply if :ref:`PDF plugin <pdf>` is installed.

    A custom binary path to rst2pdf. E.g. '/usr/bin/rst2pdf'

.. confval:: WALIKI_CODEMIRROR_SETTINGS

    A dictionary (converted to json) used to `configure Codemirror <http://codemirror.net/doc/manual.html#config>`_. The default is:

    .. code-block:: python

        {'theme': 'mbo', 'autofocus': True, 'lineNumbers': True}

.. confval:: WALIKI_RENDER_403

   If ``True``, raise an HTTP 403 (Forbidden error) if an authenticated user is not allowed to edit a page. Default is ``True``.

.. confval:: WALIKI_PAGINATE_BY

   The numbers of items per page in paginated lists, for example "what changed". Default is ``20``.

.. confval:: WALIKI_COMMITTER_EMAIL

    If :ref:`git` is enabled and anonymous editios allowed, this is the git's committer email used. Default is ``waliki@waliki.pythonanywhere.com``.


.. confval:: WALIKI_COMMITTER_NAME

    Analog to :confval:`WALIKI_COMMITTER_EMAIL`. Default is ``Waliki``

.. confval:: WALIKI_CACHE_TIMEOUT

    The maximum expiration time for a page cache, in seconds. Default is ``60*60*24`` (i.e. 1 day)

.. confval:: WALIKI_ATTACHMENTS_DIR

   If :ref:`attachments` is enabled, this is the path where uploaded files are stored.

   By default it's ``<project_root>/waliki_attachments``. Ensure the path exists and it's writable by your web server.

.. confval:: WALIKI_UPLOAD_TO_PATTERN

   The pattern used in the path relative to :confval:`WALIKI_ATTACHMENTS_DIR` to store uploaded files. It's interpolated with the following dictionary:

   .. code-block:: python

        {'slug': instance.page.slug,
        'page_id': getattr(instance.page, 'id', ''),
        'filename': filename,
        'filename_extension': os.path.splitext(filename)[1]}

    Default is ``'%(slug)s/%(filename)s'``

.. confval:: WALIKI_RST_DIRECTIVES

    List of string poiting to modules with ``register_directive()`` function that register
    extra reStructuredText Directives. Default is ``['waliki.directives.embed']``

    Check `embed.py <https://github.com/mgaitan/waliki/blob/master/waliki/directives/embed.py>`_  as an example.

.. confval:: WALIKI_RST_TRANSFORMS

    List of string poiting to reStructuredText extra Transforms classes to be applied

    Check `transforms.py <https://github.com/mgaitan/waliki/blob/master/waliki/directives/transforms.py>`_  as an example.

    Default is ``['waliki.directives.transforms.Emojis']``

.. confval:: WALIKI_USE_MATHJAX

    If ``True``, load Mathjax's assets from the official CDN service
    Default is ``False``. Check the :ref:`faq <math>` for details.

