.. :changelog:

Changelog
---------

0.4dev
++++++

under development


0.3.3 (2014-11-24)
++++++++++++++++++

- Tracking page redirections
- fix bugs related to attachments in `sync_waliki`
- The edition form uses crispy forms if it's installed
- many small improvements to help the integration/customization


0.3.2 (2014-11-17)
++++++++++++++++++

- Url pattern is configurable now. By default allow uppercase and underscores
- Added ``moin_migration_cleanup``, a tool to cleanup the result of a moin2git_ import
- Improve git parsers for *page history* and *what changed*

.. _moin2git: https://github.com/mgaitan/moin2git


0.3.1 (2014-11-11)
++++++++++++++++++

- Plugin *attachments*
- Implemented *per namespace* ACL rules
- Added the ``waliki_box`` templatetag: use waliki content in any app
- Added ``entry_point`` to extend templates from plugins
- Added a webhook to pull and sync change from a remote repository (Git)
- Fixed a bug in git that left the repo unclean

0.2 (2014-09-29)
++++++++++++++++

- Support concurrent edition
- Added a simple ACL system
- ``i18n`` support (and locales for ``es``)
- Editor based in Codemirror
- Migrated templates to Bootstrap 3
- Added the management command ``waliki_sync``
- Added a basic test suite and setup Travis CI.
- Added "What changed" page (from Git)
- Plugins can register links in the nabvar (``{% navbar_links %}``)

0.1.2 / 0.1.3 (2014-10-02)
++++++++++++++++++++++++++

* "Get as PDF" plugin
* rst2html5 fixes

0.1.1 (2014-10-02)
++++++++++++++++++

* Many Python 2/3 compatibility fixes

0.1.0 (2014-10-01)
++++++++++++++++++

* First release on PyPI.