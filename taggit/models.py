from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.db import models, IntegrityError
from django.template.defaultfilters import slugify

try:
    from transmeta import TransMeta
    TRANSMETA_AVAILABLE = True
except:
    TRANSMETA_AVAILABLE = False

class Tag(models.Model):
    if TRANSMETA_AVAILABLE:
        __metaclass__ = TransMeta

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
    
    class Meta:
        if TRANSMETA_AVAILABLE:
            translate = ('name',)

    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.slug:
            if TRANSMETA_AVAILABLE:
                self.slug = slug = slugify(getattr(self, 'name_' + settings.LANGUAGE_CODE.lower()))
            else:
                self.slug = slug = slugify(self.name)
            i = 0
            while True:
                try:
                    return super(Tag, self).save(*args, **kwargs)
                except IntegrityError:
                    i += 1
                    self.slug = "%s_%d" % (slug, i)
        else:
            return super(Tag, self).save(*args, **kwargs)


class TaggedItem(models.Model):
    object_id = models.IntegerField()
    content_type = models.ForeignKey(ContentType, related_name="tagged_items")
    content_object = GenericForeignKey()
    
    tag = models.ForeignKey(Tag, related_name="items")
    
    def __unicode__(self):
        return "%s tagged with %s" % (self.content_object, self.tag)
