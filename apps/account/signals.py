from django.db.models.signals import post_save, post_delete
from .models import User, Profile, StateUser, StateUserComment
from django.dispatch import receiver
from PIL import Image
from apps.search.models import *
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify

def image_profile(sender,instance,**kwargs):
    try:
        imagen = Image.open(instance.avatar.path)
        if imagen.size > (500,500):
            imagen.thumbnail((500,500))
        if imagen.format == 'PNG':
            bg = Image.new("RGB", imagen.size, (255,255,255))
            bg.paste(imagen,imagen)
            bg.save(instance.avatar.path)
        else:
            imagen.save(instance.avatar.path)
    except Exception as e:
        pass

post_save.connect(image_profile,sender=User)

def image_banner(sender,instance,**kwargs):
    imagen = Image.open(instance.banner.path)
    if imagen.size > (1500,1500):
        imagen.thumbnail((1500,1500))
    if imagen.format == 'PNG':
        bg = Image.new("RGB", imagen.size, (255,255,255))
        bg.paste(imagen,imagen)
        bg.save(instance.banner.path)
    else:
        imagen.save(instance.banner.path)

post_save.connect(image_banner,sender=Profile)

def remove_index(sender,instance, **kwargs):
    ctype = ContentType.objects.get_for_model(instance)
    Index.objects.get(object_id=instance.id, content_type=ctype).delete()
post_delete.connect(remove_index,sender=User)

def index_model(sender,instance,**kwargs):
    text =slugify(("%s-%s-%s")%(instance.first_name, instance.last_name, instance.username))
    Index.objects.create(instance=instance, text=text)
post_save.connect(index_model,sender=User)

def image_state(sender,instance,**kwargs):
    try:
        if instance.picture:
            imagen = Image.open(instance.picture.path)
            if imagen.size > (800,800):
                imagen.thumbnail((800,800))
            if imagen.format == 'PNG':
                bg = Image.new("RGB", imagen.size, (255,255,255))
                bg.paste(imagen,imagen)
                bg.save(instance.picture.path)
            else:
                imagen.save(instance.picture.path)
    except Exception as e:
        pass

post_save.connect(image_state,sender=StateUser)

def image_state_comment(sender,instance,**kwargs):
    try:
        if instance.picture:
            imagen = Image.open(instance.picture.path)
            if imagen.size > (800,800):
                imagen.thumbnail((800,800))
            if imagen.format == 'PNG':
                bg = Image.new("RGB", imagen.size, (255,255,255))
                bg.paste(imagen,imagen)
                bg.save(instance.picture.path)
            else:
                imagen.save(instance.picture.path)
    except Exception as e:
        pass

post_save.connect(image_state_comment,sender=StateUserComment)
