from django.db.models.signals import post_save, post_delete
from .models import FarmProfile, Farm
from django.dispatch import receiver
from PIL import Image
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify

def image_profile(sender,instance,**kwargs):
    try:
        imagen = Image.open(instance.logo.path)
        print imagen.format
        if imagen.size > (500,500):
            imagen.thumbnail((500,500))
        if imagen.format == 'PNG':
            imagen.thumbnail((500,500))
            bg = Image.new("RGB", imagen.size, (255,255,255))
            bg.paste(imagen,imagen)
            bg.save(instance.logo.path)
        elif imagen.format == 'GIF':
            imagen.thumbnail((500,500))
            imagen.convert('RGB').save(instance.logo.path, 'JPEG')
        else:
            imagen.save(instance.logo.path)
        print imagen.format
    except Exception as e:
        print e

post_save.connect(image_profile,sender=Farm)

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

post_save.connect(image_banner,sender=FarmProfile)

def remove_index(sender,instance, **kwargs):
    from apps.search.models import Index
    ctype = ContentType.objects.get_for_model(instance)
    Index.objects.get(object_id=instance.id, content_type=ctype).delete()
post_delete.connect(remove_index,sender=FarmProfile)

def index_model(sender,instance,**kwargs):
    from apps.search.models import Index
    try:
        profile = FarmProfile.objects.get(farm=instance)
        text =slugify(("%s-%s")%(instance.name, profile.slogan))
        Index.objects.create(instance=profile, text=text)
    except:
        pass
post_save.connect(index_model,sender=Farm)

def index_model_profile(sender,instance,**kwargs):
    from apps.search.models import Index
    text =slugify(("%s-%s")%(instance.farm.name, instance.slogan))
    Index.objects.create(instance=instance, text=text)
post_save.connect(index_model_profile,sender=FarmProfile)
