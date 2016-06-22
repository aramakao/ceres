from django.db.models.signals import post_delete, post_save
from .models import Blog
import os
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify

def del_image(sender,instance,**kwargs):
    if instance.image != 'blog/no_image.png':
        os.remove(instance.image.path)
post_delete.connect(del_image,sender=Blog)

def remove_index(sender,instance, **kwargs):
    from apps.search.models import Index
    ctype = ContentType.objects.get_for_model(instance)
    Index.objects.get(object_id=instance.id, content_type=ctype).delete()
post_delete.connect(remove_index,sender=Blog)

def index_model(sender,instance,**kwargs):
    from apps.search.models import Index
    text =slugify(("%s-%s")%(instance.title, instance.category.name))
    Index.objects.create(instance=instance, text=text)
post_save.connect(index_model,sender=Blog)
