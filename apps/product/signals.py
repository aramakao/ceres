from django.db.models.signals import post_save, post_delete
from .models import *
from django.dispatch import receiver
from PIL import Image
import os
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.models import ContentType

def image_product(sender,instance,**kwargs):
    try:
        imagen = Image.open(instance.image.path)
        imagen.thumbnail((800,800))
        if imagen.format == 'PNG':
            bg = Image.new("RGB", (800,800), (255,255,255))
            bg.paste(imagen,imagen)
            bg.save(instance.image.path)
        else:
            imagen.save(instance.image.path)
    except Exception as e:
        pass

def del_image(sender,instance,**kwargs):
    os.remove(instance.image.path)

post_save.connect(image_product,sender=ProductImage)
post_delete.connect(del_image,sender=ProductImage)

def image_category(sender,instance,**kwargs):
    try:
        imagen = Image.open(instance.image.path)
        imagen.thumbnail((800,400))
        if imagen.format == 'PNG':
            bg = Image.new("RGB", (800,400), (255,255,255))
            bg.paste(imagen,imagen)
            bg.save(instance.image.path)
        else:
            imagen.save(instance.image.path)
    except Exception as e:
        pass

def del_category(sender,instance,**kwargs):
    os.remove(instance.image.path)

post_save.connect(image_category,sender=ProductCategory)
post_delete.connect(del_category,sender=ProductCategory)

def remove_index(sender,instance, **kwargs):
    from apps.search.models import Index
    ctype = ContentType.objects.get_for_model(instance)
    Index.objects.get(object_id=instance.id, content_type=ctype).delete()
post_delete.connect(remove_index,sender=Product)

def index_model(sender,instance,**kwargs):
    from apps.search.models import Index
    text =slugify(("%s-%s-%s")%(instance.name, instance.summary, instance.category.name))
    Index.objects.create(instance=instance, text=text)
post_save.connect(index_model,sender=Product)
