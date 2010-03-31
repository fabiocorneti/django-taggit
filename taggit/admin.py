from django.contrib import admin
from taggit.models import Tag, TaggedItem

class TaggedItemInline(admin.TabularInline):
    model = TaggedItem
    list_display = ['get_absolute_url',]

class TagAdmin(admin.ModelAdmin):
    pass

admin.site.register(Tag, TagAdmin)
