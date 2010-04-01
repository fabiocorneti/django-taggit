from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from django.contrib import admin
from django.db.models import Q
from django.http import HttpResponse
from django.utils import simplejson
from django.utils import translation
from taggit.models import Tag
from taggit.models import TagContext
from taggit.models import TaggedItem
from taggit.utils import TRANSMETA_AVAILABLE
from taggit.utils import default_language_fieldname

class TaggedItemInline(admin.TabularInline):
    model = TaggedItem
    
class TagAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline,]
    list_filter = ('context',)
    prepopulated_fields = {'slug': [default_language_fieldname('name'),],}

    def get_urls(self):
        urls = super(TagAdmin, self).get_urls()
        admin_urls = patterns('',
            url(r'^json/completions/$', self.admin_site.admin_view(self.json_tags), {}, name="taggit-json-tags"),
        )
        return admin_urls + urls

    def json_tags(self, request):
        """
        Returns completions for the partial tag name specified in the "partial" POST parameter; 
        the format of the response is::
        
            [
                ['primary key of tag', 'name of tag'],
                ['primary key of tag', 'name of tag'],
            ]
        """
        json_tags = []
        search = request.POST.get('search', None)
        search_query = Q(name__icontains=search) | Q(context__name__icontains=search)
        if TRANSMETA_AVAILABLE:
            search_query = Q(**{'name_' + translation.get_language().lower() + '__icontains': search}) | Q(**{'context__name_' + translation.get_language().lower() + '__icontains': search})
        if not (search in [None, '']):
            for tag in Tag.objects.filter(search_query).iterator():
                json_tags.append([unicode(tag), unicode(tag)])
        return HttpResponse(simplejson.dumps(json_tags, ensure_ascii=False), mimetype='text/javascript')

class TagContextAdmin(admin.ModelAdmin):    
    prepopulated_fields = {'slug': [default_language_fieldname('name'),],}

admin.site.register(TagContext, TagContextAdmin)
admin.site.register(Tag, TagAdmin)
