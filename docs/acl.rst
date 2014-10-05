The access control system
=========================

Waliki has a very simple *"per slug"* `ACL <http://en.wikipedia.org/wiki/Access_control_list>`_ system builtin, that allow to control who have access to view, add, change or delete pages (and possible other permissions and objects) in your wiki.

It's inspired in `django-guardian <https://github.com/lukaszb/django-guardian>`_` and leverages on ``django.contrib.auth``.

You can define your ACL policies defining default permissions
for anonymous and logged users in your settings (``WALIKI_ANONYMOUS_USER_PERMISSIONS`` and ``WALIKI_LOGGED_USER_PERMISSIONS``) and instances of the model ``ACLRules`` that stores:

    - which permissions the rule gives
    - to which groups and/or users
    - limited to which slug

So, here is how it works:

- Access controlled views has a decorator :func:`acl.permission_required`
  that asks the user for one or more permissions **in that specific slug** to access
- The decorator checks if there is an ACL rule with the requested
  permission/s that apply to this slug.
- If there is a rule and the user is in the rule's allowed users (because
  it was explicitly assigned or because it belongs to a group assigned to the rule), then the user will be able access
- If there isn't a matching rule, check Waliki's defaults permissions
- Lastly, check standard user's *per model* permissions.

An example
----------

You want this:

- Anonymous users can view any page except the
  ones under the slug *intranet*. Anonymous users can't edit pages.
- Identified users are allowed to see and edit any page, even the ones under
  the slug *intranet*, but they aren't allowed to edit the page with slug
  *home* (the homepage) nor delete any page
- The user *john* and any user from the group *editors* can edit the home
- Only superusers can delete pages.

So, first, by default anonymous users only have ``view_page`` permission,
and logged in users can also edit but not delete. In your settings::


    WALIKI_ANONYMOUS_USER_PERMISSIONS = ('view_page', )
    WALIKI_LOGGED_USER_PERMISSIONS = ('view_page', 'add_page', 'change_page')

Then go to the admin an create the following rules:

- One rule for the slug **intranet** with the permissions
  ``view_page``, ``add_page`` and ``change_page``. In "Apply to" select *Any logged in user*
- Another rule for the homepage: slug *home* (or the slug defined
  in ``WALIKI_HOME_SLUG``), with permission ``delete_page``, applied to *Any user/group explicitly defined*,
  and add the user *jhon* and the group *editors* respectively
- Lastly, add a rule for the delete permissions to superusers



