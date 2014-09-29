import os.path
import importlib
import collections
from django.conf import settings
from .utils import get_url
from waliki.rst2html5 import HTML5Writer


def _get_default_data_dir():
    settings_mod = importlib.import_module(settings.SETTINGS_MODULE)
    project_dir = os.path.abspath(os.path.dirname(settings_mod.__name__))
    return os.path.join(project_dir, 'waliki_data')


def deep_update(d, u):
    """update nested dicts. if u is a dict and hasn't a key, the original is keeped
    inspired in Alex Martelli's
    http://stackoverflow.com/a/3233356"""
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            r = deep_update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


def _get_markup_settings(user_settings):
    defaults = {'reStructuredText': {
                    'settings_overrides': {              # noqa
                        'initial_header_level': 2,
                        'record_dependencies': True,
                        'stylesheet_path': None,
                        'link_stylesheet': True,
                        'syntax_highlight': 'short'},
                    'writer': HTML5Writer(),
                    'writer_name': 'html5'
                    },
                'Markdown': {
                    'extensions': ['wikilinks', 'headerid'],
                    'extension_configs': {
                        'wikilinks': {'build_url': get_url},
                        'headerid': {'level': 2},
                    }
                }
            }

    deep_update(defaults, user_settings)
    return defaults

WALIKI_AVAILABLE_MARKUPS = getattr(settings, 'WALIKI_AVAILABLE_MARKUPS', ['reStructuredText', 'Markdown'])

# options: reStructuredText, Markdown, Textile
WALIKI_DEFAULT_MARKUP = WALIKI_AVAILABLE_MARKUPS[0]

# your content folder. by default it's <project_root>/waliki_data
WALIKI_DATA_DIR = getattr(settings, 'WALIKI_DATA_DIR', None) or _get_default_data_dir()

# wich page is shown as the wiki index?
WALIKI_INDEX_SLUG = getattr(settings, 'WALIKI_INDEX_SLUG', "home")

# kwargs for each markup.
WALIKI_MARKUPS_SETTINGS = _get_markup_settings(getattr(settings, 'WALIKI_MARKUPS_SETTINGS', {}))

# get as txt
WALIKI_PDF_INCLUDE_TITLE = getattr(settings, 'WALIKI_PDF_INCLUDE_TITLE', False)

WALIKI_CODEMIRROR_SETTINGS = getattr(settings, 'WALIKI_CODEMIRROR_SETTINGS',
                                     {'lineNumbers': False, 'theme': 'monokai', 'autofocus': True})

# ('view_page', 'add_page', 'change_page', 'delete_page')
WALIKI_ANONYMOUS_USER_PERMISSIONS = getattr(settings, 'WALIKI_ANONYMOUS_USER_PERMISSIONS',
                                            ('view_page',))

WALIKI_LOGGED_USER_PERMISSIONS = getattr(settings, 'WALIKI_LOGGED_USER_PERMISSIONS',
                                         ('view_page', 'add_page', 'change_page'))

WALIKI_RENDER_403 = getattr(settings, 'WALIKI_RENDER_403', True)


WALIKI_COMMITTER_EMAIL = getattr(settings, 'WALIKI_COMMITTER_EMAIL', 'waliki@waliki.pythonanywhere.com')

WALIKI_COMMITTER_NAME = getattr(settings, 'WALIKI_COMMITTER_NAME', 'Waliki')
