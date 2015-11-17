from django.test import TestCase
from django.core.urlresolvers import reverse
from .factories import PageFactory
from waliki.settings import WALIKI_DATA_DIR
from waliki.models import Page
from waliki.git import Git
import json
import os
import shutil
from sh import git
git = git.bake("--no-pager", _tty_out=False)


class TestGitWebhook(TestCase):

    def setUp(self):
        self.content = "- item"
        self.page = PageFactory(path="page.rst", raw=self.content)
        Git().commit(self.page)
        self.remote = self.set_remote(True)
        self.url = reverse('waliki_webhook_pull', args=('origin',))

    def set_remote(self, chdir=False):
        # init
        remote = WALIKI_DATA_DIR + '_remote'
        git.clone(WALIKI_DATA_DIR, remote)
        os.chdir(remote)
        git.config("user.email", 'somebody@tolove.com')
        git.config("user.name", 'I am me, yo')

        os.chdir(WALIKI_DATA_DIR)
        git.remote('add', 'origin', remote)
        if chdir:
            os.chdir(remote)
        return remote

    def tearDown(self):
        try:
            shutil.rmtree(WALIKI_DATA_DIR)
            shutil.rmtree(self.remote)
        except FileNotFoundError:
            pass

    def test_edit_file_no_conflict(self):
        # commit remotely
        with open("page.rst", 'w') as p:
            p.write(self.content + '\nhey! edited remotely!\n')
        git.add('.')
        git.commit('-m', 'a remote log')
        # webhook post (this would be done externally)
        response = self.client.post(self.url, {})

        self.assertEqual(self.page.raw, self.content + '\nhey! edited remotely!\n')
        pull_stdout = json.loads(response.content.decode('utf8'))['pull']
        self.assertIn('1 file changed', pull_stdout)

    def test_edit_file_with_a_conflict(self):
        # commit remotely
        with open("page.rst", 'w') as p:
            p.write(self.content + '\nremote line')
        git.add('.')
        git.commit('-m', 'a remote log')

        # meanwhile. commit a change
        self.page.raw = self.page.raw + '\nlocal line'
        Git().commit(self.page)
        response = self.client.post(self.url, {})
        # local wins
        # Note: newer versions of git don't leave a blank line at the end
        self.assertRegexpMatches(self.content + "\nlocal line\n?$", self.page.raw)

    def test_create_page_if_remote_added_files(self):
        assert not Page.objects.filter(path="newpage.rst").exists()
        with open("newpage.rst", 'w') as p:
            p.write('the new content')
        git.add('.')
        git.commit('-m', 'add new page')
        response = self.client.post(self.url, {})
        # now exists
        new_page = Page.objects.get(path="newpage.rst")
        self.assertEqual(new_page.raw, 'the new content')

    def test_remote_delete_a_page(self):
        git.rm(self.page.path)
        git.commit('-m', 'delete page')
        response = self.client.post(self.url, {})
        self.assertEqual(Page.objects.count(), 0)
