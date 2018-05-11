from django import VERSION
from django.test import TestCase
if VERSION[:2] >= (1, 10):
    from django.urls import reverse
else:
    from django.core.urlresolvers import reverse
from .factories import PageFactory, RedirectFactory


class TestPageRedirect(TestCase):

	def test_simple_redirect(self):
		page = PageFactory(slug='hello')
		RedirectFactory(old_slug='bye', new_slug='hello')
		response = self.client.get(reverse('waliki_detail', args=('bye',)))
		self.assertRedirects(response, page.get_absolute_url(),
							 status_code=302, target_status_code=200)



