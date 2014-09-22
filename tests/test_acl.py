from .factories import UserFactory, GroupFactory, ACLRuleFactory
from waliki.models import ACLRule
from django.test import TestCase


class TestGetUsersRules(TestCase):

    def test_simple_user(self):
        user = UserFactory()
        slug = 'page'
        rule = ACLRuleFactory(slug=slug, permission='view_page', users=[user])
        users = ACLRule.get_users_for('view_page', 'page')
        self.assertEqual(list(users), [user])



