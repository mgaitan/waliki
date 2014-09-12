from django.utils.text import slugify

def get_slug(text):
    return '/'.join(slugify(t) for t in text.split('/'))

