import sys
import shutil
import tempfile

WALIKI_DATA_DIR = tempfile.mkdtemp()

try:
    from django.conf import settings

    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            }
        },
        ROOT_URLCONF="waliki.urls",
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.sites",
            "django.contrib.staticfiles",
            "waliki",
            "waliki.git"
        ],
        MIDDLEWARE_CLASSES=(
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ),
        STATIC_URL='/static/',
        SITE_ID=1,
        NOSE_ARGS=['-s', '--nologcapture', '--nocapture',
                   '--with-id', '--logging-clear-handlers'],
        WALIKI_DATA_DIR=WALIKI_DATA_DIR,
        WALIKI_ANONYMOUS_USER_PERMISSIONS = ('view_page', 'add_page', 'change_page')
    )

    try:
        import django
        setup = django.setup
    except AttributeError:
        pass
    else:
        setup()

    from django_nose import NoseTestSuiteRunner
except ImportError:
    raise ImportError(
        "To fix this error, run: pip install -r requirements-test.txt")


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # Run tests
    test_runner = NoseTestSuiteRunner(verbosity=1)

    failures = test_runner.run_tests(test_args)

    shutil.rmtree(WALIKI_DATA_DIR)
    if failures:
        sys.exit(failures)


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
