.. _acl:

The access control system
=========================

Waliki has a very simple *"per slug"* `Access Control List <http://en.wikipedia.org/wiki/Access_control_list>`_ system built-in, that allows to control who has access to view, add, change or delete pages (and possible other permissions and objects) in your wiki.

It's inspired in `django-guardian <https://github.com/lukaszb/django-guardian>`_ and leverages on ``django.contrib.auth``.

You can define your ACL policies defining default permissions
for anonymous and logged users in your settings (``WALIKI_ANONYMOUS_USER_PERMISSIONS`` and ``WALIKI_LOGGED_USER_PERMISSIONS``) and instances of the model :class:`ACLRule`` that stores:

- which permissions the rule gives
- to which groups and/or users
- limited to which slug

So, here is how it works:

- Access controlled views have a decorator :func:`acl.permission_required`
  that asks the user for one or more permissions **in that specific slug** to access the view.
- The decorator checks if there is an ACL rule with the requested
  permission/s that apply to this slug.
- If there is a rule and the user is in the rule's allowed users (because
  it was explicitly assigned or because it belongs to a group assigned to the rule), then the user will be able to access
- If there isn't a matching rule, check Waliki's defaults permissions
- Lastly, check standard user's *per model* permissions.

Example
----------

Suppose you want this policy:

- Anonymous users can view any page except the
  ones under the slug *intranet*. Anonymous users can't edit pages.
- Identified users are allowed to see and edit any page, even the ones under
  the slug *intranet*, but they aren't allowed to edit the page with slug
  *home* (the homepage) nor to delete any pages
- The user *john* and any user from the group *editors* can edit the home
- Only superusers can delete pages.

So, first, by default, anonymous users only have ``view_page`` permission,
and logged in users can also edit but not delete. In your settings:

.. code-block:: python

    WALIKI_ANONYMOUS_USER_PERMISSIONS = ('view_page', )
    WALIKI_LOGGED_USER_PERMISSIONS = ('view_page', 'add_page', 'change_page')

.. note:: Note that, in this case, those are the Waliki's
          defaults permissions, so, you wouldn't need to set them.
          Check :confval:`WALIKI_ANONYMOUS_USER_PERMISSIONS` and :confval:`WALIKI_LOGGED_USER_PERMISSIONS` for further details.

Then go to the admin an create the following rules:

- One rule for the slug **intranet** with the permissions
  ``view_page``, ``add_page`` and ``change_page``. In "Apply to" select *Any authenticated user*
- Add a rule for the homepage: slug *home* (or the slug defined
  in ``WALIKI_INDEX_SLUG``), with the permission ``add_page`` and ``change_page``, apply to *Any user/group explicitly defined*, and add the user *jhon* and the group *editors* respectively.
- Lastly, add a rule for the permission ``delete_page`` and apply it to
  *Any superusers*



Checking permissions in your plugins
------------------------------------

If you are writing your own plugin, you can use the ACL reusing the view decorator. For example:

.. code-block:: python

    from waliki.acl import permission_required

    @permission_required('view_page')
    def your_read_only_view(request, slug):
        ...

    @permission_required(['change_page', 'add_page'])
    def your_read_write_view(request, slug):
        ...

.. attention:: When a view requires more than one permission, at least one
               rule with **all those permissions** should apply to the user.

               For example, if the rule *A* gives to *user1* the permission ``change_page`` and the rule *B* gives to *user1* the permission
               ``delete_page``, *user1* is still not allowed to request a view that requires both ``change_page`` and ``delete_page``.


Also, you can use the low-level helper :func:`acl.check_perms`:

.. code-block:: python

    if check_perms(('edit_page'), request.user, page.slug):
        do_something()

To check permissions in a template, you can use the templatetag :func:`waliki_tags.check_perms`

.. attention::

    Make sure you have ``django.core.context_processors.request`` in your ``TEMPLATE_CONTEXT_PROCESSORS`` setting to use contextual variables
    like ``request.user``


The format is::

    {% check_perms "perm1[, perm2, ...]" for user in slug as "context_var" %}

or::

    {% check_perms "perm1[, perm2, ...]" for user in "slug" as "context_var" %}


For example (assuming ``page`` objects are available from *context*)

.. code-block:: html

    {% load waliki_tags %}

    {% check_perms "delete_page" for request.user in page.slug as "can_delete" %}
    {% if can_delete %}
        <a id="confirmDelete" class="text-error">Delete</a>
    {% endif %}


