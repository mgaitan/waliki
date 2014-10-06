Boxes: Waliki as a (dummy) CMS
==============================

The templatetag :func:`waliki_box` allow to render a wiki page content as a portion (a "box") of a webpage, and allow a rapid edition if the user has the right permission.

The templatetag receives the page slug as only parameter::

    {% waliki_box "page/slug" %}

Usage example
-------------

Consider a view that render a template:

.. code-block:: python

    urlpatterns = patterns('',
        ...
        url(r'^boxes-example/', TemplateView.as_view(template_name="boxes_example.html")),
        ...
    )

Where ``boxes_example.html`` is as following:

.. code-block:: html

    {% extends "base.html" %}
    {% load waliki_tags %}

    {% block body %}
        <h1>Waliki boxes example</h1>

            <div class="row" style="margin-top: 50px">
                <div class="col-sm-8">
                    {% waliki_box "boxes/left" %}
                </div>
                <div class="col-sm-4">
                    {% waliki_box "boxes/right" %}
                </div>
            </div>
            <hr>
            <div class="row">
                <div class="col-lg-12">
                    {% waliki_box "boxes/footer/"|add:request.user.username %}
                </div>
            </div>
        </div>

    {% endblock %}

You can `see this example <http://waliki.pythonanywhere.com/boxes-example/>` live in the demo site. Note that the demo site apply an :ref:`ACL rule <acl_>`
to limit the edition of the any block under the *namespace* ``boxes``  to authenticated users.

`Login <http://waliki.pythonanywhere.com/accounts/login/?next=/boxes-example/>`_ to edit the boxes!

.. tip:: As you can see in the code of the template, the last box is all yours,
         because it will render "boxes/footer/<your_username>" :)




