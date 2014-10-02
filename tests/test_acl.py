from .factories import UserFactory, GroupFactory, ACLRuleFactory
from waliki.models import ACLRule
from django.test import TestCase
from django.template import Template, Context, TemplateSyntaxError


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
        ACLRuleFactory(slug='page', permissions=['change_page'], users=[user1])
        users = ACLRule.get_users_for(['view_page', 'change_page'], 'page')
        self.assertEqual(set(users), {user1})


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
