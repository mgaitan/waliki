from django.test import TestCase
from django.template import Template, Context, TemplateSyntaxError
from django.contrib.auth.models import AnonymousUser
from mock import patch
from waliki.models import ACLRule
from waliki.acl import check_perms
from .factories import UserFactory, GroupFactory, ACLRuleFactory


class TestGetUsersRules(TestCase):

    def test_simple_user(self):
        user = UserFactory()
        ACLRuleFactory(slug='page', permissions=['view_page'], users=[user])
        users = ACLRule.get_users_for('view_page', 'page')
        self.assertEqual(set(users), {user})

    def test_simple_group(self):
        group_users = [UserFactory(), UserFactory()]
        group = GroupFactory(users=group_users)
        ACLRuleFactory(slug='page', permissions=['view_page'], groups=[group])
        users = ACLRule.get_users_for('view_page', 'page')
        self.assertEqual(set(users), set(group_users))

    def test_mixing_group_and_users(self):
        user = UserFactory()
        group1_users = [UserFactory(), UserFactory()]
        group2_users = [UserFactory(), UserFactory()]
        group1 = GroupFactory(users=group1_users)
        group2 = GroupFactory(users=group2_users)
        ACLRuleFactory(slug='page', permissions=['view_page'],
                       groups=[group1, group2], users=[user])
        users = ACLRule.get_users_for('view_page', 'page')
        self.assertEqual(set(users), set(group1_users + group2_users + [user]))

    def test_is_distinct(self):
        user = UserFactory()
        group1_users = [user]
        group1 = GroupFactory(users=group1_users)
        ACLRuleFactory(slug='page', permissions=['view_page'],
                       groups=[group1], users=[user])
        users = ACLRule.get_users_for('view_page', 'page')
        self.assertEqual(users.count(), 1)
        self.assertEqual(set(users), set(group1_users))

    def test_simple_user_for_multiples_perms(self):
        user1 = UserFactory()
        user2 = UserFactory()
        ACLRuleFactory(
            slug='page', permissions=['view_page'], users=[user1, user2])
        ACLRuleFactory(slug='page', permissions=['view_page', 'change_page'], users=[user1])
        users = ACLRule.get_users_for(['view_page', 'change_page'], 'page')
        self.assertEqual(set(users), {user1})

    def test_any_user(self):
        user1 = UserFactory()
        ACLRuleFactory(slug='page', permissions=['view_page'], apply_to=ACLRule.TO_ANY)
        users = ACLRule.get_users_for(['view_page'], 'page')
        self.assertIn(AnonymousUser(), users)
        self.assertIn(user1, users)

    def test_any_logged_user(self):
        user1 = UserFactory()
        ACLRuleFactory(slug='page', permissions=['view_page'], apply_to=ACLRule.TO_LOGGED)
        users = ACLRule.get_users_for(['view_page'], 'page')
        self.assertNotIn(AnonymousUser(), users)
        self.assertIn(user1, users)

    def test_to_staff(self):
        UserFactory()
        user2 = UserFactory(is_staff=True)
        ACLRuleFactory(slug='page', permissions=['view_page'], apply_to=ACLRule.TO_STAFF)
        users = ACLRule.get_users_for(['view_page'], 'page')
        self.assertEqual(set(users), {user2})

    def test_to_super(self):
        UserFactory()
        UserFactory(is_staff=True)
        user2 = UserFactory(is_superuser=True)
        ACLRuleFactory(slug='page', permissions=['change_page'], apply_to=ACLRule.TO_SUPERUSERS)
        users = ACLRule.get_users_for(['change_page'], 'page')
        self.assertEqual(set(users), {user2})


class TestNamespaces(TestCase):

    def test_simple_namespace(self):
        user1 = UserFactory()
        user2 = UserFactory()
        ACLRuleFactory(slug='user1-section', permissions=['change_page'],
                       as_namespace=True, users=[user1])
        self.assertTrue(check_perms('change_page', user1, 'user1-section'))
        self.assertTrue(check_perms('change_page', user1, 'user1-section/nested/page'))
        self.assertFalse(check_perms('change_page', user2, 'user1-section'))
        self.assertFalse(check_perms('change_page', user2, 'user1-section/nested/page'))

    def test_two_levels_namespace(self):
        user1 = UserFactory()
        user2 = UserFactory()
        ACLRuleFactory(slug='section/special', permissions=['change_page'],
                       as_namespace=True, users=[user1])
        self.assertTrue(check_perms('change_page', user1, 'section/special'))
        self.assertTrue(check_perms('change_page', user1, 'section/special/page'))
        self.assertTrue(check_perms('change_page', user2, 'section/no-special'))
        self.assertFalse(check_perms('change_page', user2, 'section/special/page'))

    def test_a_section_for_staff(self):
        user = UserFactory()
        staff_member = UserFactory(is_staff=True)
        ACLRuleFactory(slug='staff-section', permissions=['view_page', 'add_page', 'change_page'],
                       as_namespace=True, apply_to=ACLRule.TO_STAFF)
        for perm in ['view_page', 'add_page', 'change_page']:
            self.assertFalse(check_perms(perm, user, 'staff-section'))
            self.assertFalse(check_perms(perm, user, 'staff-section/a-page'))
            self.assertTrue(check_perms(perm, staff_member, 'staff-section'))
            self.assertTrue(check_perms(perm, staff_member, 'staff-section/a-page'))


class CheckPermTagTest(TestCase):

    def render_template(self, template, context):
        """
        Returns rendered ``template`` with ``context``, which are given as string
        and dict respectively.
        """
        t = Template(template)
        return t.render(Context(context))

    def test_wrong_formats(self):
        wrong_formats = (
            # no quotes
            '{% check_perms "view_page" for user in slug as has_perm %}',
            # wrong quotes
            '{% check_perms "view_page" for user in slug as \'has_perms" %}',
            # wrong quotes
            '{% check_perms view_page for user in slug as "has_perms" %}',
            # wrong quotes
            '{% check_perms "view_page, change_page for user in slug as "has_perms" %}',
            # wrong quotes
            '{% check_perms "view_page" user in slug as "has_perms" %}',
            # no context_var
            '{% check_perms "view_page" for user in slug as %}',
            # no slug
            '{% check_perms "view_page" for user as "has_perms" %}',
            # no user
            '{% check_perms "view_page" in slug as "has_perms" %}',
            # no "for" bit
            '{% check_perms "view_page, change_page" user in slug as "has_perms" %}',
            # no "as" bit
            '{% check_perms "view_page" for user in slug "has_perms" %}',
        )
        context = {'user': UserFactory(), 'slug': "any/slug"}
        for wrong in wrong_formats:
            fullwrong = '{% load waliki_tags %}' + wrong
            with self.assertRaises(TemplateSyntaxError):
                self.render_template(fullwrong, context)

    def test_check_users_is_called(self):
        template = """
        {% load waliki_tags %}
        {% check_perms "view_page" for user in slug as "has_perms" %}
        {{ has_perms }}
        """
        user = UserFactory()
        slug = 'any/slug'
        context = {'user': user, 'slug': slug}

        with patch('waliki.templatetags.waliki_tags.check_perms_helper') as check:
            check.return_value = "return_value"
            output = self.render_template(template, context)
        check.assert_called_once_with(["view_page"], user, slug)
        self.assertEqual(output.strip(), 'return_value')

    def test_check_users_is_called_with_multiple(self):
        template = """
        {% load waliki_tags %}
        {% check_perms "x, y,z" for user in slug as "has_perms" %}
        {{ has_perms }}
        """
        user = UserFactory()
        slug = 'any/slug'
        context = {'user': user, 'slug': slug}

        with patch('waliki.templatetags.waliki_tags.check_perms_helper') as check:
            check.return_value = "return_value"
            output = self.render_template(template, context)
        check.assert_called_once_with(["x", "y", "z"], user, slug)
        self.assertEqual(output.strip(), 'return_value')

    def test_check_users_is_called_slug_literal(self):
        template = """
        {% load waliki_tags %}
        {% check_perms "x, y,z" for user in "literal_slug" as "has_perms" %}
        {{ has_perms }}
        """
        user = UserFactory()
        context = {'user': user}
        with patch('waliki.templatetags.waliki_tags.check_perms_helper') as check:
            check.return_value = "return_value"
            output = self.render_template(template, context)
        check.assert_called_once_with(["x", "y", "z"], user, "literal_slug")
        self.assertEqual(output.strip(), 'return_value')
