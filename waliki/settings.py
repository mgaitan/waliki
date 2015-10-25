import os.path
from importlib import import_module
import collections
from django.conf import settings
from .utils import get_url
from waliki.rst2html5 import HTML5Writer
try:
    from django.utils.module_loading import import_string
except ImportError:
    # django 1.6
    from django.utils.module_loading import import_by_path as import_string


def _get_default_data_dir(directory, abspath=True):
    settings_mod = import_module(settings.SETTINGS_MODULE)

    project_dir = os.path.dirname(settings_mod.__name__)
    if abspath:
        project_dir = os.path.abspath(project_dir)
    return os.path.join(project_dir, directory)


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
                    # check http://docutils.sourceforge.net/docs/user/config.html
                    'settings_overrides': {              # noqa
                        'initial_header_level': 2,
                        'record_dependencies': True,
                        'stylesheet_path': None,
                        'link_stylesheet': True,
                        'syntax_highlight': 'short',
                        'halt_level': 5,
                    },
                    'writer': HTML5Writer(),
                    'writer_name': 'html5',
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


WALIKI_SLUG_PATTERN = getattr(settings, 'WALIKI_SLUG_PATTERN', '[a-zA-Z0-9-_\/]+')

WALIKI_SLUGIFY_FUNCTION = getattr(settings, 'WALIKI_SLUGIFY_FUNCTION', 'waliki.utils.get_slug')

WALIKI_SANITIZE_FUNCTION = getattr(settings, 'WALIKI_SANITIZE_FUNCTION', 'waliki.utils.sanitize')

get_slug = import_string(WALIKI_SLUGIFY_FUNCTION)
sanitize = import_string(WALIKI_SANITIZE_FUNCTION)


# your content folder. by default it's <project_root>/waliki_data
WALIKI_DATA_DIR = getattr(settings, 'WALIKI_DATA_DIR', None) or _get_default_data_dir('waliki_data')

# wich page is shown as the wiki index?
WALIKI_INDEX_SLUG = getattr(settings, 'WALIKI_INDEX_SLUG', "home")

# kwargs for each markup.
WALIKI_MARKUPS_SETTINGS = _get_markup_settings(getattr(settings, 'WALIKI_MARKUPS_SETTINGS', {}))

# get as txt
WALIKI_PDF_INCLUDE_TITLE = getattr(settings, 'WALIKI_PDF_INCLUDE_TITLE', False)

# custom rst2pdf binary path. You should set it on python3.
WALIKI_PDF_RST2PDF_BIN = getattr(settings, 'WALIKI_PDF_RST2PDF_BIN', False)

WALIKI_CODEMIRROR_SETTINGS = getattr(settings, 'WALIKI_CODEMIRROR_SETTINGS',
                                     {'lineNumbers': False, 'theme': 'mbo', 'autofocus': True, 'lineNumbers': True})

# ('view_page', 'add_page', 'change_page', 'delete_page')
WALIKI_ANONYMOUS_USER_PERMISSIONS = getattr(settings, 'WALIKI_ANONYMOUS_USER_PERMISSIONS',
                                            ('view_page',))

WALIKI_LOGGED_USER_PERMISSIONS = getattr(settings, 'WALIKI_LOGGED_USER_PERMISSIONS',
                                         ('view_page', 'add_page', 'change_page'))

WALIKI_RENDER_403 = getattr(settings, 'WALIKI_RENDER_403', True)

WALIKI_PAGINATE_BY = getattr(settings, 'WALIKI_PAGINATE_BY', 20)

WALIKI_COMMITTER_EMAIL = getattr(settings, 'WALIKI_COMMITTER_EMAIL', 'waliki@waliki.pythonanywhere.com')

WALIKI_COMMITTER_NAME = getattr(settings, 'WALIKI_COMMITTER_NAME', 'Waliki')

WALIKI_CACHE_TIMEOUT = getattr(settings, 'WALIKI_CACHE_TIMEOUT', 60*60*24)

WALIKI_ATTACHMENTS_DIR = getattr(settings, 'WALIKI_ATTACHMENTS_DIR', None)  or _get_default_data_dir('waliki_attachments', False)

WALIKI_UPLOAD_TO_PATTERN = '%(slug)s/%(filename)s'

WALIKI_RST_DIRECTIVES = getattr(settings, 'WALIKI_RST_DIRECTIVES', ['waliki.directives.embed'])

WALIKI_RST_TRANSFORMS = getattr(settings, 'WALIKI_RST_TRANSFORMS', ['waliki.directives.transforms.Emojis'])

WALIKI_USE_MATHJAX = getattr(settings, 'WALIKI_USE_MATHJAX', False)

WALIKI_BREADCRUMBS = getattr(settings, 'WALIKI_BREADCRUMBS', False)


def WALIKI_UPLOAD_TO(instance, filename):
    return os.path.join(WALIKI_ATTACHMENTS_DIR,
                        WALIKI_UPLOAD_TO_PATTERN % {'slug': instance.page.slug,
                                                       'page_id': getattr(instance.page, 'id', ''),
                                                       'filename': filename,
                                                       'filename_extension': os.path.splitext(filename)[1]})

for mod in WALIKI_RST_DIRECTIVES:
    register_directive = import_string(mod + '.register_directive')
    register_directive()
