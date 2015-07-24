from django.utils.translation import ugettext_lazy as _

from waliki import views
from waliki.models import Page
from waliki.signals import page_preedit
from waliki.views import edit

import json
from rest_framework import serializers, request
from rest_framework.exceptions import PermissionDenied


class PageRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializer Class to retrieve a Page.
    """
    class Meta():
        model = Page
        fields = ('id', 'title', 'slug', 'raw', 'markup', )
        read_only_fields = fields


class PageListRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializer class to show a list of Pages
    """

    class Meta():
        model = Page
        fields = ('id', 'title', 'slug', )
        read_only_fields = ('id', 'title', 'slug', )


class PageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer Class to create a Page.
    """
    
    def save(self, *args, **kwargs):
        """call to waliki new function"""
        #call waliki new function
        response = views.new(self.context['request']._request, *args, **kwargs)


    class Meta():
        model = Page
        fields = ('id', 'title', 'slug', 'markup' )
        read_only_fields = ('id', )


class PageEditSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer Class to edit a Page.
    """
    raw = serializers.CharField()
    message = serializers.CharField(write_only=True)
    extra_data = serializers.SerializerMethodField()


    def get_extra_data(self, page):
        form_extra_data = {}
        receivers_responses = page_preedit.send(sender=edit, page=page)
        for r in receivers_responses:
            if isinstance(r[1], dict) and 'form_extra_data' in r[1]:
                form_extra_data.update(r[1]['form_extra_data'])
        return json.dumps(form_extra_data)


    def save(self, *args, **kwargs):
        """call to waliki edit function"""
        #call waliki new function        
        #if 'extra_data' no comming in payload
        if not self.context['request'].POST.get('extra_data', False):
            mutable = self.context['request'].POST._mutable
            self.context['request'].POST._mutable = True
            self.context['request'].POST['extra_data'] = self.get_extra_data(self.instance)
            self.context['request'].POST._mutable = mutable

        kwargs['slug'] = self.instance.slug

        response = views.edit(self.context['request'],*args, **kwargs)


    class Meta():
        model = Page
        fields = ('id', 'title', 'slug', 'raw', 'markup' ,'message', 'extra_data', )
        read_only_fields = ('id', 'slug', )


class PageDeleteSerializer(serializers.ModelSerializer):
    """
    Serializer Class to delete a Page or namespace.
    """
    
    what = serializers.ChoiceField(
        choices=(
            ('this', _('Just this page')),
            ('namespace', _('This page and all the namespace')))
        )

    class Meta():
        model = Page
        fields = ('id', 'title', 'slug', 'what')
        read_only_fields = fields


class PageMoveSerializer(serializers.ModelSerializer):
    """
    Serializer Class to move a page.
    """
    class Meta():
        model = Page
        fields = ('slug', )