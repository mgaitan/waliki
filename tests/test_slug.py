from unittest import TestCase
from waliki.utils import get_slug


class TestDefaultSlug(TestCase):

	def test_basic(self):
		self.assertEqual(get_slug('hello'), 'hello')

	def test_spaces(self):
		self.assertEqual(get_slug('hello world'), 'hello-world')

	def test_multi_spaces(self):
		self.assertEqual(get_slug('hello     world'), 'hello-world')

	def test_camel_case_keep_as_is(self):
		self.assertEqual(get_slug('HelloWorld'), 'HelloWorld')


	def test_subdirectory(self):
		self.assertEqual(get_slug('nested/page'), 'nested/page')

	def test_subdirectory_with_spaces(self):
		self.assertEqual(get_slug('nested/page with spaces'), 'nested/page-with-spaces')

	def test_underscore(self):
		self.assertEqual(get_slug('page_with underscore'), 'page_with-underscore')




