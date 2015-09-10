from django.core.urlresolvers import reverse
from django.conf import settings

from rest_framework import status
from rest_framework.test import APITestCase

from waliki.models import Page


class PageCreateTests(APITestCase):
    
    def test_create_page_anonymous(self):
        """
        #Ensure a new Page can't be created by a Anonymous user without permission
        """
        url = reverse('page_new')
        data = {'title': 'Title', 'slug':'title', 'markup': 'Markdown'}
        response = self.client.post(url, data)

        if 'add_page' in settings.WALIKI_ANONYMOUS_USER_PERMISSIONS:
            #if anonymous user can add page
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)  
        else:
            #anonymous user can't add page
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PageRetrieveTests(APITestCase):
    title = 'My little Title'
    slug = 'my-little-title'
    markup = 'Markdown'

    raw = 'My hack'
    message = 'Fuck you'

    def setUp(self):
        Page.objects.create(title=self.title, slug=self.slug, markup=self.markup)
    
    def test_detail_page_anonymous(self):
        """
        Ensure a Page can't be watched by a Anonymous user without permission
        """
        url = reverse('page_detail', args=(self.slug,))
        response = self.client.get(url)

        if 'view_page' in settings.WALIKI_ANONYMOUS_USER_PERMISSIONS:
            #if anonymous user can view a page
            self.assertEqual(response.status_code, status.HTTP_200_OK)  
        else:
            #if anonymous user can't view a page
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  


class PageEditTests(APITestCase):
    title = 'My little Title'
    slug = 'my-little-title'
    markup = 'Markdown'

    raw = 'My hack'
    message = 'Fuck you'

    def setUp(self):
        Page.objects.create(title=self.title, slug=self.slug, markup=self.markup)

    def test_edit_page_anonymous(self):
        """
        #Ensure a Page can't be edited by a Anonymous user without permission
        """
        url = reverse('page_edit', args=(self.slug,))
        data = {
            'title': self.title,
            'slug': self.slug,
            'markup': self.markup,
            'raw': self.raw,
            'message': self.message }
        
        response = self.client.post(url, data)

        if 'change_page' in settings.WALIKI_ANONYMOUS_USER_PERMISSIONS:
            #if anonymous user can view a page
            self.assertEqual(response.status_code, status.HTTP_200_OK)  
        else:
            #if anonymous user can't view a page
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_move_page_anonymous(self):
        """
        #Ensure a Page can't be moved by a Anonymous user without permission
        """
        url = reverse('page_move', args=(self.slug,))
        data = {
            'slug': 'self-slug'
            }
        
        response = self.client.post(url, data)

        if 'change_page' in settings.WALIKI_ANONYMOUS_USER_PERMISSIONS:
            #if anonymous user can view a page
            self.assertEqual(response.status_code, status.HTTP_200_OK)  
        else:
            #if anonymous user can't view a page
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_page_anonymous(self):
        """
        #Ensure a Page can't be deleted by a Anonymous user without permission
        """
        url = reverse('page_delete', args=(self.slug,))
        data = {
            'what': 'this'
            }       
        response = self.client.post(url, data)

        if 'change_page' in settings.WALIKI_ANONYMOUS_USER_PERMISSIONS:
            #if anonymous user can view a page
            self.assertEqual(response.status_code, status.HTTP_200_OK)  
        else:
            #if anonymous user can't view a page
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  
