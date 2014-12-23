A tale on Waliki's history
==========================

 In june of 2013 I tweeted this:

.. raw:: html

   <blockquote class="twitter-tweet"><p>Is there any wiki engine that uses <a href="https://twitter.com/search?q=%23restructuredText&amp;src=hash">#restructuredText</a> as its core markup? Everything I found is incomplete or not working hacks</p>&mdash; Martín Gaitán (@tin_nqn_) <a href="https://twitter.com/tin_nqn_/statuses/350238674803363842">June 27, 2013</a></blockquote><script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

When the master `Roberto Alsina`_ offered to convert Alva_ in a wiki system someday I asked him this:

.. _Roberto Alsina: http://www.ralsina.com.ar
.. _Alva: http://donewithniko.la/

.. raw:: html

   <blockquote class="twitter-tweet"><p><a href="https://twitter.com/tin_nqn_">@tin_nqn_</a> sure: <a href="https://t.co/Z377dGfw88">https://t.co/Z377dGfw88</a></p>&mdash; Roberto Alsina (@ralsina) <a href="https://twitter.com/ralsina/statuses/350247679168745475">June 27, 2013</a></blockquote><script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

That was the beginning. I found and forked a tiny `wiki system <https://github.com/alexex/wiki>`_ based on Flask and sent a first `pull request <https://github.com/alexex/wiki/pull/30>`_ where I explained a few of my motivations:

    I've researched for a while, looking for a simple, yet usable, wiki engine with support for reStructuredText, since it's in what I write fluently and what I can use to render with Sphinx (de facto standard documentation tool in the python ecosystem), rst2pdf or whatever

    Few wikis like MoinMoin or the builtin wiki in Trac have this feature, but processing a "block of restructuredtext" in the middle of another core markup.

    Even when this project uses markdown, it's so simple to refactor this "render function" as a config option.

During those days, I started to take a lot of design decisions and committed a bunch of code, so my fork diverged too much from Alex's wiki. That's how the `original version of Waliki <https://github.com/mgaitan/waliki_flask/>`_ was born.

Waliki reborn
-------------

I was happy with the result but blocked to continue. As a newbie in Flask, each attempted step was a challenge, and I was not sure whether to be faithful to the conventions: my brain was too *djangonized*.

Moreover, the `Python Argentina web project <https://github.com/PyAr/pyarweb>`_ needed a wiki engine based on Django.

So, I decided to redo it, taking as much code and as many ideas as possible. It took some time, but it's here :).


.. include:: ../HISTORY.rst
