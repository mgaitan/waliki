import os.path
import importlib
import collections
from django.conf import settings
from .utils import get_url
from .rst2html5 import HTML5Writer


def _get_default_data_dir():
    settings_mod = importlib.import_module(settings.SETTINGS_MODULE)
    project_dir = os.path.abspath(os.path.dirname(settings_mod.__name__))
    return os.path.join(project_dir, 'waliki_data')


def _get_markup_settings(user_settings):

    defaults = {'reStructuredText': {
                    'settings_overrides': {              # noqa
                        'initial_header_level': 2,
                        'record_dependencies': True,
                        'stylesheet_path': None,
                        'link_stylesheet': True,
                        'syntax_highlight': 'short'},
                    'writer': HTML5Writer(),
                    },
                'Markdown': {
                    'extensions': ['wikilinks', 'headerid'],
                    'extensions_config': {
                        'wikilinks': [('build_url', get_url)],
                        'headerid': [('level', 2)]},
                    }
                }

    for k, v in user_settings.items():
        if isinstance(v, collections.Mapping):
            r = user_settings(defaults.get(k, {}), v)
            defaults[k] = r
        else:
            defaults[k] = user_settings[k]
    return defaults


# your content folder. by default it's <project_root>/waliki_data
WALIKI_DATA_DIR = getattr(settings, 'WALIKI_DATA_DIR', _get_default_data_dir())

# options: reStructuredText, Markdown, Textile
WALIKI_DEFAULT_MARKUP = getattr(settings, 'WALIKI_DEFAULT_MARKUP', "reStructuredText")

# wich page is shown as the wiki index?
WALIKI_INDEX_SLUG = getattr(settings, 'WALIKI_INDEX_SLUG', "home")

# kwargs for each markup.
WALIKI_MARKUPS_SETTINGS = _get_markup_settings(getattr(settings, 'WALIKI_MARKUPS_SETTINGS', {}))
