#-*- encoding: utf-8 -*-
from django.db.models.signals import post_save
from .models import *
from .tasks import *

def SendEmail(sender,instance,**kwargs):
    send_email.delay(instance)
post_save.connect(SendEmail,sender=Message)
