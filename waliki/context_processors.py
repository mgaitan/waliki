
def settings(request):
    """inject few waliki's settings to the context  to be used in templates"""
    from waliki.settings import WALIKI_USE_MATHJAX      # NOQA
    return {k: v for (k, v) in locals().items() if k.startswith('WALIKI')}
