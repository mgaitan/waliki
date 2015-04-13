from django.dispatch import receiver
from waliki.models import Page
from django.db.models.signals import post_save
from django.core.cache import cache

######################################################
# SIGNAL HANDLERS
######################################################

@receiver(post_save, sender=Page)
def on_page_save_clear_slide_cache(instance, **kwargs):
    cache.delete(instance.get_cache_key('slides'))
