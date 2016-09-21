from django.contrib import admin
from .models import Query, Result


class QueryClassAdmin(admin.ModelAdmin):
    list_display = ['id', 'query', 'status', ]
    list_display_links = ['id', ]
    list_editable = ['query', 'status', ]
    list_filter = ['status', ]
    empty_value_display = 'Empty'
    actions_on_top = True

    fieldsets = (
        (None, {'fields': (('query', 'status',),)}),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('query', 'status',),
            'description': '<b>This is description<b>'})
    )


class ResultClassAdmin(admin.ModelAdmin):
    list_display = ['id', 'query', 'url', 'spider', 'date', 'rang', ]
    list_display_links = ['id', 'query', 'spider', 'rang',]
    list_filter = ['spider', 'rang', ]
    empty_value_display = 'Empty'
    actions_on_top = True

    fieldsets = (
        (None, {'fields': ('query', 'url', ('spider', 'date', 'rang',),)}),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('query', 'url', 'spider', 'date', 'rang',),
            'description': '<b>This is description<b>'})
    )

admin.site.register(Query, QueryClassAdmin)
admin.site.register(Result, ResultClassAdmin)
