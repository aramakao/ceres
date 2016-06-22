#-*- encoding: utf-8 -*-
from django.db.models.signals import post_save
from .models import *
from django.core.urlresolvers import reverse
from apps.ceres.notification import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.contrib.sites.models import Site
from .tasks import *

def sendNotificationProductComment(sender,instance,**kwargs):
    if not instance.reply:
        notificationAskProduct(instance.buyer, instance.seller, instance)
    else:
        notificationReplyProduct(instance.seller, instance.buyer, instance)
post_save.connect(sendNotificationProductComment,sender=ProductComments)

def SendEmailNewOrder(sender,instance,**kwargs):
    send_email_new_order.delay(instance)
post_save.connect(SendEmailNewOrder,sender=PurchaseOrder)

def SendEmailRecordOrder(sender,instance,**kwargs):
    send_email_order.delay(instance)
post_save.connect(SendEmailRecordOrder,sender=PurchaseRecord)

def SendEmailMailbox(sender,instance,**kwargs):
    if instance.email and instance.reply:
        send_email_mailbox.delay(instance)
post_save.connect(SendEmailMailbox,sender=Mailbox)
