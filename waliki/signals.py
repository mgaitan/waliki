import django.dispatch

page_preedit = django.dispatch.Signal(providing_args=["page"])
page_saved = django.dispatch.Signal(providing_args=["raw", "author", "message"])
