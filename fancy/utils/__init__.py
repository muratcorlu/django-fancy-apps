from django.template.defaultfilters import slugify as slugify_original
from django.db.models.signals import post_save
from django.dispatch import receiver
from taggit.models import TaggedItem

def slugify(value):
    value = value.replace(u'\u0131', 'i')
    return slugify_original(value)

@receiver(post_save)
def delete_image_files(sender, instance, **kwargs):
    if sender == TaggedItem:
        instance.tag.slug = slugify(instance.tag.name)
        instance.tag.save()
