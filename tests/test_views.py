import mock
from django.test import TestCase
from waliki.models import Page
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from waliki import settings
from .factories import PageFactory, UserFactory, ACLRuleFactory


class TestPageView(TestCase):


    def setUp(self):
        self.page = PageFactory(raw="hello test!")
        self.edit_url = reverse('waliki_edit', args=(self.page.slug,))

    def test_view(self):
        response = self.client.get(self.page.get_absolute_url())
        self.assertContains(response, self.page.title)
        self.assertContains(response, self.page.body)
        self.assertContains(response, self.edit_url)
        self.assertTemplateUsed(response, 'waliki/detail.html')

    def test_view_raw(self):
        response = self.client.get(self.page.get_absolute_url() + '/raw')
        self.assertContains(response, self.page.raw)
        self.assertEqual(response['Content-Type'], 'text/plain; charset=utf-8')

    def test_view_no_perm_no_auth(self):
        with mock.patch('waliki.acl.WALIKI_ANONYMOUS_USER_PERMISSIONS', return_value=()):
            response = self.client.get(self.page.get_absolute_url())
        self.assertRedirects(response, '/accounts/login/?next=' + self.page.get_absolute_url())

    def test_view_auth(self):
        user = UserFactory()
        self.client.login(username=user.username, password='pass')
        with mock.patch('waliki.acl.WALIKI_ANONYMOUS_USER_PERMISSIONS', return_value=()):
            response = self.client.get(self.page.get_absolute_url())
        self.assertContains(response, self.page.body)
        self.assertContains(response, self.edit_url)
        self.assertTemplateUsed(response, 'waliki/detail.html')

    def test_view_auth_no_perms(self):
        user = UserFactory()

        self.client.login(username=user.username, password='pass')
        with mock.patch('waliki.acl.WALIKI_ANONYMOUS_USER_PERMISSIONS'):
            with mock.patch('waliki.acl.WALIKI_LOGGED_USER_PERMISSIONS'):
                response = self.client.get(self.page.get_absolute_url())
        self.assertTemplateUsed(response, 'waliki/403.html')
        self.assertEqual(response.status_code, 403)
