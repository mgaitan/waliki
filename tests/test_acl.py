from .factories import UserFactory, GroupFactory, ACLRuleFactory
from waliki.models import ACLRule
from django.test import TestCase


class TestGetUsersRules(TestCase):

    def test_simple_user(self):
        user = UserFactory()
        ACLRuleFactory(slug='page', permission='view_page', users=[user])
        users = ACLRule.get_users_for('view_page', 'page')
        self.assertEqual(set(users), {user})

    def test_simple_group(self):
        group_users = [UserFactory(), UserFactory()]
        group = GroupFactory(users=group_users)
        ACLRuleFactory(slug='page', permission='view_page', groups=[group])
        users = ACLRule.get_users_for('view_page', 'page')
        self.assertEqual(set(users), set(group_users))

    def test_mixing_group_and_users(self):
        user = UserFactory()
        group1_users = [UserFactory(), UserFactory()]
        group2_users = [UserFactory(), UserFactory()]
        group1 = GroupFactory(users=group1_users)
        group2 = GroupFactory(users=group2_users)
        ACLRuleFactory(slug='page', permission='view_page',
                       groups=[group1, group2], users=[user])
        users = ACLRule.get_users_for('view_page', 'page')
        self.assertEqual(set(users), set(group1_users + group2_users + [user]))
