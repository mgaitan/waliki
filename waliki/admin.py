from django.contrib import admin
from .models import Page, ACLRule

# Register your models here.
admin.site.register(Page)
admin.site.register(ACLRule)

