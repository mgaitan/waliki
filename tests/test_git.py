from django.test import TestCase
from sh import git
from django.core.urlresolvers import reverse
from waliki.models import Page
from waliki.git import Git
from .factories import PageFactory


class TestGit(TestCase):

    def setUp(self):
        self.page = PageFactory()
        self.edit_url = reverse('waliki_edit', args=(self.page.slug,))

    def test_commit_existent_page_with_no_previous_commits(self):
        response = self.client.get(self.edit_url)
        data = response.context[0]['form'].initial
        data["raw"] = "test content"
        data["message"] = "testing :)"
        response = self.client.post(self.edit_url, data)
        self.assertEqual(self.page.raw, "test content")
        self.assertEqual(Git().version(self.page, 'HEAD'), "test content")
        self.assertIn("testing :)", git.log('-s', '--format=%s', self.page.path))

    def test_commit_new_page(self):
        assert not Page.objects.filter(slug='test').exists()
        url = reverse('waliki_edit', args=('test',))
        response = self.client.get(url)
        # it exists now
        self.assertTrue(Page.objects.filter(slug='test').exists())
        data = response.context[0]['form'].initial
        data["raw"] = "hey there\n"
        data["title"] = "Test Page"
        data["message"] = ""
        response = self.client.post(url, data)
        page = Page.objects.get(slug='test')
        self.assertEqual(page.title, "Test Page")
        self.assertEqual(page.raw, "hey there\n")
        self.assertEqual(Git().version(page, 'HEAD'), "hey there\n")


