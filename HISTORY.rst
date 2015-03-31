.. :changelog:

Changelog
---------

0.4 (2015-03-31)
++++++++++++++++

**Implemented enhancements:**

- Implemented views to add a new, move and delete pages
- Implemented real-time collaborative editing via together.js
  (`#33 <https://github.com/mgaitan/waliki/issues/33>`__)
- Added pagination in *what changed* page
- Added a way to extend waliki's docutils with directives and transformation for
- A deep docs proofreading by `chuna <https://github.com/chuna>`__

**Closed issues:**

- Edit view redirect to detail if the page doesn't exist
  (`#37 <https://github.com/mgaitan/waliki/issues/37>`__)
-  waliki\_box fails with missing slug
   `#40 <https://github.com/mgaitan/waliki/issues/40>`__
-  can't view diffs on LMDE
   `#60 <https://github.com/mgaitan/waliki/issues/60>`__

-  fix typos in tutorial
   `#76 <https://github.com/mgaitan/waliki/pull/76>`__
   (`martenson <https://github.com/martenson>`__)

-  Fix build with Markups 0.6.
   `#63 <https://github.com/mgaitan/waliki/pull/63>`__
   (`loganchien <https://github.com/loganchien>`__)

-  fixed roundoff error for whatchanged pagination
   `#61 <https://github.com/mgaitan/waliki/pull/61>`__
   (`aszepieniec <https://github.com/aszepieniec>`__)

-  Enhance slides `#59 <https://github.com/mgaitan/waliki/pull/59>`__
   (`loganchien <https://github.com/loganchien>`__)

-  Fix UnicodeDecodeError in waliki.git.view.
   `#58 <https://github.com/mgaitan/waliki/pull/58>`__
   (`loganchien <https://github.com/loganchien>`__)



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