import json
import os
import mock
from django.test import TestCase
from waliki.models import Page
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.template.loader import render_to_string
from waliki import settings
from waliki.models import Redirect
from waliki.forms import MovePageForm, DeleteForm

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



class TestPageEdit(TestCase):

    def setUp(self):
        self.page = PageFactory(raw="hello test!")
        self.edit_url = reverse('waliki_edit', args=(self.page.slug,))

    def test_edit_form_use_page_instance(self):
        response = self.client.get(self.edit_url)
        self.assertEqual(response.context[0]['form'].instance, self.page)

    def test_get_edit_not_existent_page_raises_404(self):
        response = self.client.get(reverse('waliki_edit', args=('unknown-page',)))
        self.assertEqual(response.status_code, 404)

    def test_post_edit_not_existent_page_create_page(self):
        assert not Page.objects.filter(slug='unknown-page').exists()
        response = self.client.post(reverse('waliki_edit', args=('unknown-page',)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Page.objects.filter(slug='unknown-page').count(), 1)


class TestMove(TestCase):

    def setUp(self):
        self.page = PageFactory(raw="hello test!", slug='a-page')
        self.move_url = reverse('waliki_move', args=(self.page.slug,))

    def test_normal_get(self):
        response = self.client.get(self.move_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'waliki/move.html')
        self.assertIsInstance(response.context[0]['form'], MovePageForm)

    def test_ajax_get(self):
        with mock.patch('waliki.views.render_to_string') as r2s_mock:
            r2s_mock.side_effect = render_to_string
            response = self.client.get(self.move_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(json.loads(response.content.decode('utf8')).keys()), ['data'])
        self.assertEqual(r2s_mock.call_args[0][0], 'waliki/move.html')

    def test_post_with_error(self):
        response = self.client.post(self.move_url, {'slug': self.page.slug})
        self.assertEqual(response.status_code, 200)
        form = response.context[0]['form']
        self.assertEqual(form.errors, {'slug': ["The slug wasn't changed"]})

    def test_post_ajax_with_error(self):
        response = self.client.post(self.move_url, {'slug': self.page.slug}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf8'))
        self.assertIn("The slug wasn", data['data'])
        self.assertNotIn('redirect', data)

    def test_success_post_move_page(self):
        with mock.patch('waliki.views.page_moved') as page_moved_mock:
            response = self.client.post(self.move_url, {'slug': 'another-page'})
        self.assertRedirects(response, reverse('waliki_detail', args=('another-page',)), status_code=302)

        page = Page.objects.get(id=self.page.id)
        self.assertEqual(page.slug, 'another-page')
        self.assertEqual(page.path, 'another-page.rst')
        self.assertIn("hello test!", open(page.abspath).read())
        page_moved_mock.assert_called_once()

    def test_success_post_ajax(self):
        with mock.patch('waliki.views.page_moved') as page_moved_mock:
            response = self.client.post(self.move_url, {'slug': 'another-page'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        page = Page.objects.get(id=self.page.id)
        self.assertEqual(page.slug, 'another-page')
        self.assertEqual(page.path, 'another-page.rst')
        data = json.loads(response.content.decode('utf8'))
        self.assertEqual(data['redirect'], page.get_absolute_url())
        self.assertIn("hello test!", open(page.abspath).read())
        page_moved_mock.assert_called_once()

    def test_can_move_to_nested_page(self):
        response = self.client.post(self.move_url, {'slug': 'another/nested/page'})
        self.assertRedirects(response, reverse('waliki_detail', args=('another/nested/page',)), status_code=302)
        page = Page.objects.get(id=self.page.id)
        self.assertIn("hello test!", open(page.abspath).read())

    def test_move_creates_a_redirection(self):
        assert not Redirect.objects.all().exists()
        self.client.post(self.move_url, {'slug': 'new-slug'})
        self.assertEqual(Redirect.objects.all().count(), 1)
        r = Redirect.objects.all()[0]
        self.assertEqual(r.old_slug, 'a-page')
        self.assertEqual(r.new_slug, 'new-slug')

    def test_move_updates_old_redirection(self):
        # a couple of redirect exists to the page we'll move
        Redirect.objects.create(old_slug='an-old-page-redirected', new_slug='a-page')
        Redirect.objects.create(old_slug='another-old-page-redirected', new_slug='a-page')
        self.client.post(self.move_url, {'slug': 'moved-slug'})
        self.assertEqual(Redirect.objects.all().count(), 3)
        self.assertEqual(Redirect.objects.get(old_slug='an-old-page-redirected').new_slug, 'moved-slug')
        self.assertEqual(Redirect.objects.get(old_slug='another-old-page-redirected').new_slug, 'moved-slug')

    def test_move_delete_redirections_targeting_new_page(self):
        Redirect.objects.create(old_slug='the-new-slug', new_slug='any')
        self.client.post(self.move_url, {'slug': 'the-new-slug'})
        self.assertEqual(Redirect.objects.all().count(), 1)
        self.assertEqual(Redirect.objects.filter(old_slug='the-new-slug').count(), 0)


class TestDelete(TestCase):

    def setUp(self):
        self.page = PageFactory(raw="hello test!", slug='a-page')
        self.delete_url = reverse('waliki_delete', args=(self.page.slug,))

    def login(self):
        self.user = UserFactory()
        ACLRuleFactory(slug='a-page', permissions=['delete_page'], users=[self.user])
        self.client.login(username=self.user.username, password='pass')

    def test_normal_get_without_permission(self):
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 302)

    def test_ajax_get_without_permission(self):
        response = self.client.get(self.delete_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 302)

    def test_normal_get_with_permission(self):
        self.login()
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'waliki/delete.html')
        self.assertIsInstance(response.context[0]['form'], DeleteForm)

    def test_ajax_get_with_permission(self):
        self.login()
        with mock.patch('waliki.views.render_to_string') as r2s_mock:
            r2s_mock.side_effect = render_to_string
            response = self.client.get(self.delete_url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(json.loads(response.content.decode('utf8')).keys()), ['data'])
        self.assertEqual(r2s_mock.call_args[0][0], 'waliki/delete.html')

    def test_successful_post_delete_only_page(self):
        self.login()
        path = self.page.abspath
        response = self.client.post(self.delete_url, {'what': 'this'})
        self.assertRedirects(response, reverse('waliki_home'), status_code=302)
        self.assertFalse(Page.objects.filter(id=self.page.id).exists())
        self.assertFalse(os.path.exists(path))

    def test_successful_post_ajax_delete_only_page(self):
        self.login()
        path = self.page.abspath
        response = self.client.post(self.delete_url, {'what': 'this'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertFalse(Page.objects.filter(id=self.page.id).exists())
        self.assertFalse(os.path.exists(path))
        data = json.loads(response.content.decode('utf8'))
        self.assertEqual(data['redirect'], reverse('waliki_home'))

    def test_successful_post_delete_only_page(self):
        self.login()
        path = self.page.abspath
        response = self.client.post(self.delete_url, {'what': 'this'})
        self.assertRedirects(response, reverse('waliki_home'), status_code=302)
        self.assertFalse(Page.objects.filter(id=self.page.id).exists())
        self.assertFalse(os.path.exists(path))

    def test_successful_post_delete_namespace(self):

        # TODO : whould we check permissions on each page?
        self.login()

        page2 = PageFactory(raw="hello test 2!", slug='a-page/subpage')
        page2_path = page2.abspath
        path = self.page.abspath
        response = self.client.post(self.delete_url, {'what': 'namespace'})
        self.assertRedirects(response, reverse('waliki_home'), status_code=302)

        self.assertFalse(Page.objects.filter(id=self.page.id).exists())
        self.assertFalse(os.path.exists(path))
        self.assertFalse(Page.objects.filter(id=page2.id).exists())
        self.assertFalse(os.path.exists(page2_path))

    def test_successful_ajax_post_delete_namespace(self):
        self.login()

        page2 = PageFactory(raw="hello test 2!", slug='a-page/subpage')
        page2_path = page2.abspath
        path = self.page.abspath
        response = self.client.post(self.delete_url, {'what': 'namespace'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        data = json.loads(response.content.decode('utf8'))
        self.assertEqual(data['redirect'], reverse('waliki_home'))

        self.assertFalse(Page.objects.filter(id=self.page.id).exists())
        self.assertFalse(os.path.exists(path))
        self.assertFalse(Page.objects.filter(id=page2.id).exists())
        self.assertFalse(os.path.exists(page2_path))
