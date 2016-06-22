from django.db.models.signals import post_save, post_delete
from .models import Group, GroupProfile
from django.dispatch import receiver
from PIL import Image
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify

def image_profile(sender,instance,**kwargs):
    try:
        imagen = Image.open(instance.logo.path)
        if imagen.size > (500,500):
            imagen.thumbnail((500,500))
        if imagen.format == 'PNG':
            bg = Image.new("RGB", imagen.size, (255,255,255))
            bg.paste(imagen,imagen)
            bg.save(instance.logo.path)
        else:
            imagen.save(instance.logo.path)
    except Exception as e:
        pass

post_save.connect(image_profile,sender=Group)

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

post_save.connect(image_banner,sender=GroupProfile)

def remove_index(sender,instance, **kwargs):
    from apps.search.models import Index
    ctype = ContentType.objects.get_for_model(instance)
    Index.objects.get(object_id=instance.id, content_type=ctype).delete()
post_delete.connect(remove_index,sender=GroupProfile)

def index_model(sender,instance,**kwargs):
    from apps.search.models import Index
    try:
        profile = GroupProfile.objects.get(group=instance)
        text =slugify(("%s-%s")%(instance.name, profile.slogan))
        Index.objects.create(instance=profile, text=text)
    except:
        pass
post_save.connect(index_model,sender=Group)

def index_model_profile(sender,instance,**kwargs):
    from apps.search.models import Index
    text =slugify(("%s-%s")%(instance.group.name, instance.slogan))
    Index.objects.create(instance=instance, text=text)
post_save.connect(index_model_profile,sender=GroupProfile)
