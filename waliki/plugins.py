# -*- coding: utf-8 -*-
"""
Credits to ojii, functions get_module and load are from:
https://github.com/ojii/django-load. Taken from django-wiki.
"""
from __future__ import print_function
from django.conf import settings
from django.utils.importlib import import_module



_cache = {}
_extra_page_actions = {}


class BasePlugin(object):
    """Plugins should inherit from this"""
    # Must fill in!
    slug = None

    # Optional
    # settings_form = None    # A form class to add to the settings tab
    urls_root = []   # General urlpatterns that will reside in waliki root
    urls_page = []    # urlpatterns that receive page slug  .../page/slug/
    extra_page_actions = {}   # {'all': (_('Attachments'), "icon-file")}



def get_module(app, modname, verbose, failfast):
    """
    Internal function to load a module from a single app.
    """
    module_name = '%s.%s' % (app, modname)
    try:
        module = import_module(module_name)
    except ImportError as e:
        if failfast:
            raise e
        elif verbose:
            print("Could not load %r from %r: %s" % (modname, app, e))
        return None
    if verbose:
        print("Loaded %r from %r" % (modname, app))
    return module


def load(modname, verbose=False, failfast=False):
    """
    Loads all modules with name 'modname' from all installed apps.
    If verbose is True, debug information will be printed to stdout.
    If failfast is True, import errors will not be surpressed.
    """
    for app in settings.INSTALLED_APPS:
        get_module(app, modname, verbose, failfast)


def load_plugins():
    load('waliki_plugin', verbose=False, failfast=False)


def register(PluginClass):
    """
    Register a plugin class. This function will call back your plugin's
    constructor.
    """
    if PluginClass in _cache.keys():
        raise Exception("Plugin class already registered")
    plugin = PluginClass()
    _cache[PluginClass] = plugin

    if getattr(PluginClass, 'extra_page_actions', None):
        for key in plugin.extra_page_actions:
            if key not in _extra_page_actions:
                _extra_page_actions[key] = []
            _extra_page_actions[key].extend(plugin.extra_page_actions[key])


def page_urls():
    return [urlpattern for p in get_plugins() for urlpattern in p.urls_page]


def root_urls():
    return [urlpattern for p in get_plugins() for urlpattern in p.urls_page]


def get_plugins():
    """Get loaded plugins - do not call before all plugins are loaded."""
    return _cache


def get_extra_page_actions():
    return _extra_page_actions
