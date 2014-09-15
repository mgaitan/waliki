import django.dispatch

page_saved = django.dispatch.Signal(providing_args=["raw", "author", "message"])
