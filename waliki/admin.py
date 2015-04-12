from django.contrib import admin
from .models import Page, ACLRule, Redirect


class PageAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'markup')
    list_filter = ('markup',)
    search_fields = ('slug', 'title')


class ACLRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'as_namespace', 'apply_to')
    list_filter = ('apply_to', 'permissions')
    search_fields = ('slug', 'name', 'users__username', 'groups__name')


class RedirectAdmin(admin.ModelAdmin):
    list_display = ('old_slug', 'new_slug', 'status_code')
    search_fields = ('old_slug', 'new_slug')


# Register your models here.
admin.site.register(Page, PageAdmin)
admin.site.register(ACLRule, ACLRuleAdmin)
admin.site.register(Redirect, RedirectAdmin)
