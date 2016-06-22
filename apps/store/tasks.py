#-*- encoding: utf-8 -*-
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from celery import shared_task

@shared_task()
def send_email_order(instance):
    try:
        if instance.state==1:
            url = reverse('order_buyer',kwargs={'pk':instance.purchase_order.id,})
            full_url = 'http://%s%s' % (Site.objects.get_current().domain,url)
            d = Context({ 'fullname': instance.purchase_order.buyer.fullName,
            'orden_id':str(instance.purchase_order.id).zfill(6),
            'url':full_url, 'message':'Has realizado una compra, orden de compra ' })
            plaintext = get_template('email/notifications.txt')
            htmly = get_template('email/notifications.html')
            to = instance.purchase_order.buyer.email
            subject = 'Nueva Compra - Orden N° %s' % str(instance.purchase_order.id).zfill(6)
            from_email = 'hello@agroceres.net'

            text_content = plaintext.render(d)
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            #####
            d = Context({ 'fullname': instance.purchase_order.farm.user.fullName,
            'orden_id':str(instance.purchase_order.id).zfill(6),
            'url':full_url, 'message':'Han realizado una compra, orden de compra ' })
            plaintext = get_template('email/notifications.txt')
            htmly = get_template('email/notifications.html')
            to = instance.purchase_order.farm.user.email
            subject = 'Nueva Compra - Orden N° %s' % str(instance.purchase_order.id).zfill(6)
            from_email = 'hello@agroceres.net'

            text_content = plaintext.render(d)
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        if instance.state==4 or instance.state==2 :
            url = reverse('order_buyer',kwargs={'pk':instance.purchase_order.id,})
            full_url = 'http://%s%s' % (Site.objects.get_current().domain,url)
            d = Context({ 'fullname': instance.purchase_order.buyer.fullName,
            'orden_id':str(instance.purchase_order.id).zfill(6),
            'url':full_url, 'message':'Tienes un nuevo mensaje en tu orden de compra ' })
            plaintext = get_template('email/notifications.txt')
            htmly = get_template('email/notifications.html')
            to = instance.purchase_order.buyer.email
            subject = 'Nuevo mensaje en la Orden N° %s' % str(instance.purchase_order.id).zfill(6)
            from_email = 'hello@agroceres.net'
            text_content = plaintext.render(d)
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

        elif instance.state==3:
            url = reverse('order_seller',kwargs={'pk':instance.purchase_order.id,})
            full_url = 'http://%s%s' % (Site.objects.get_current().domain,url)
            d = Context({ 'fullname': instance.purchase_order.farm.user.fullName,
            'orden_id':str(instance.purchase_order.id).zfill(6),
            'url':full_url,
            'message':'Tienes un nuevo mensaje en tu orden de compra ' })
            plaintext = get_template('email/notifications.txt')
            htmly = get_template('email/notifications.html')
            to = instance.purchase_order.farm.user.email
            subject = 'Nuevo mensaje en la Orden N° %s' % str(instance.purchase_order.id).zfill(6)
            from_email = 'hello@agroceres.net'
            text_content = plaintext.render(d)
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
    except Exception as e:
        print e
        pass

@shared_task()
def send_email_new_order(order):
    try:
        url = reverse('order_seller',kwargs={'pk':order.id,})
        full_url = 'http://%s%s' % (Site.objects.get_current().domain,url)
        d = Context({ 'fullname': order.farm.user.fullName,
        'orden_id':str(order.id).zfill(6),
        'url':full_url,
        'message':'Tienes un nueva venta!!! Orden de compra ' })
        plaintext = get_template('email/notifications.txt')
        htmly = get_template('email/notifications.html')
        to = order.farm.user.email
        subject = 'Nueva Compra, Orden N° %s' % str(order.id).zfill(6)
        from_email = 'hello@agroceres.net'
        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception as e:
        print e
        pass

@shared_task()
def send_email_mailbox(mailbox):
    try:
        d = Context({ 'reply': mailbox.reply, 'name':mailbox.user })
        plaintext = get_template('email/mailbox.txt')
        htmly = get_template('email/mailbox.html')
        to = mailbox.email
        subject = 'AgroCeres - Buzón de Sugerencias'
        from_email = 'hello@agroceres.net'
        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception as e:
        print e
        pass
