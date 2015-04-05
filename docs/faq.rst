.. _faq:

Frequently Asked Questions
==========================

Which is the biggest site powered by Waliki?
    It's the `Python Argentina Community's wiki <http://python.org.ar/wiki/ >`_ . It
    was migrated to Waliki from MoinMoin in March 2015.

    It has more than 1000 pages and few active users.

Does Waliki scale?
    May be, but huge wiki site are not the Waliki's target.

    My main concern about the Waliki's "scalability" is on how many concurrent users may it support and how slow is to save a page..

    The *"git commit per edition"* is cool, I'm happy with the *merge-instead-block* approach for concurrent editions, but it could be a boottleneck for a high traffic wiki.

    I guess it could be improved in the future, using libgit2 instead of plain system calls to the git cli.

Can Waliki render math?
    Sure! Both reStructuredText and Markdown play well with Mathjax. As the Mathjax's assets (javascript file) are huge, it's disable by default.
    To enable it you need add ``waliki.context_processors.settings`` to ``TEMPLATE_CONTEXT_PROCESSORS`` and set ``WALIKI_USE_MATHJAX`` to ``True`` in your settings::

        TEMPLATE_CONTEXT_PROCESSORS = (
            ...
            "waliki.context_processors.settings"
        )

        WALIKI_USE_MATHJAX = True

Does it use some cache?
    Yes, it uses the builtin `django's cache framework  <https://docs.djangoproject.com/en/dev/topics/cache/>`_ . The cache is invalidated automatically when a page is modified.
    The default cache timeout is 1 day, but you can override it setting ``WALIKI_CACHE_TIMEOUT``
    (in seconds). For example::

        WALIKI_CACHE_TIMEOUT = 3600    # 1 hour cache