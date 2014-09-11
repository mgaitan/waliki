import collections
from django.conf import settings


def _get_default_data_dir():
    import importlib
    import os.path
    settings_mod = importlib.import_module(settings.SETTINGS_MODULE)
    project_dir = os.path.abspath(os.path.dirname(settings_mod.__name__))
    return os.path.join(project_dir, 'waliki_data')


def _get_markup_settings(user_settings):
    defaults = {'reStructuredText': {
                    'initial_header_level': 2,
                    'record_dependencies': True,
                    'stylesheet_path': None,
                    'link_stylesheet': True,
                    'syntax_highlight': 'short'}
                }
    try:
        from rst2html5 import HTML5Writer
        defaults['reStructuredText']['writer'] = HTML5Writer()
    except ImportError:
        pass

    for k, v in user_settings.items():
        if isinstance(v, collections.Mapping):
            r = user_settings(defaults.get(k, {}), v)
            defaults[k] = r
        else:
            defaults[k] = user_settings[k]
    return defaults


WALIKI_DEFAULT_MARKUP = getattr(settings, 'WALIKI_DEFAULT_MARKUP', "reStructuredText")
WALIKI_INDEX_SLUG = getattr(settings, 'WALIKI_INDEX_SLUG', "home")
WALIKI_DATA_DIR = getattr(settings, 'WALIKI_DATA_DIR', _get_default_data_dir())
WALIKI_MARKUPS_SETTINGS = _get_markup_settings(getattr(settings, 'WALIKI_MARKUPS_SETTINGS', {}))
