from django.contrib import admin
from taggit.models import Tag, TaggedItem

class TaggedItemInline(admin.TabularInline):
    model = TaggedItem

class TagAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline,]

admin.site.register(Tag, TagAdmin)
