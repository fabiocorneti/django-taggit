from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.db import models, IntegrityError
from django.template.defaultfilters import slugify
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

try:
    from transmeta import TransMeta
    TRANSMETA_AVAILABLE = True
except:
    TRANSMETA_AVAILABLE = False

class TagContext(models.Model):
    """
    A tag context.
    
    Contexts can be used to categorize tags; for example, tags representing 
    colors could be associated to a Color context to generate navigation 
    hierarchies or filters::
    
    TagContext     Color
        Tag            Red
        Tag            Green
        Tag            Blue
    
    They can also be used to resolve tag ambiguity::
    
    TagContext     Car
        Tag            Jaguar

    TagContext     Animal
        Tag            Jaguar

    TagContext     Car
        Tag            Jaguar

    TagContext     Animal
        Tag            Jaguar
    """
    if TRANSMETA_AVAILABLE:
        __metaclass__ = TransMeta

    name = models.CharField(max_length=255, verbose_name=_(u"Name"))
    slug = models.SlugField(unique=True, max_length=255, verbose_name=_(u"Slug"))
    
    class Meta:
        verbose_name = _(u"Tag context")
        verbose_name_plural = _(u"Tag contexts")
        if TRANSMETA_AVAILABLE:
            translate = ('name',)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk and not self.slug:
            if TRANSMETA_AVAILABLE:
                self.slug = slug = slugify(getattr(self, 'name_' + translation.get_language().lower()))
            else:
                self.slug = slug = slugify(self.name)
            i = 0
            while True:
                try:
                    return super(TagContext, self).save(*args, **kwargs)
                except IntegrityError:
                    i += 1
                    self.slug = "%s_%d" % (slug, i)
        else:
            return super(TagContext, self).save(*args, **kwargs)

class Tag(models.Model):
    if TRANSMETA_AVAILABLE:
        __metaclass__ = TransMeta

    name = models.CharField(max_length=100, verbose_name=_(u"Name"))
    slug = models.SlugField(unique=True, max_length=100, verbose_name=_(u"Slug"))
    
    class Meta:
        verbose_name = _(u"Tag")
        verbose_name_plural = _(u"Tags")
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
    object_id = models.IntegerField(verbose_name=_(u"Object ID"))
    content_type = models.ForeignKey(ContentType, related_name="tagged_items", verbose_name=_(u"Content type"))
    content_object = GenericForeignKey()
    
    tag = models.ForeignKey(Tag, related_name="items", verbose_name=_(u"Tag"))
    
    class Meta:
        verbose_name = _(u"Tagged item")
        verbose_name_plural = _(u"Tagged items")

    def __unicode__(self):
        return _("%(content_object)s tagged with %(tag)s") % {'content_object': self.content_object, 'tag': self.tag}
