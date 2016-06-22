from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from celery import shared_task

@shared_task()
def send_email(instance):
    try:
        url = reverse('message_app:message',kwargs={'username':instance.sender.username,})
        full_url = 'http://%s%s' % (Site.objects.get_current().domain,url)
        d = Context({ 'fullname': instance.receiver.fullName ,'url':full_url,
        'message':'Tienes un nuevo mensaje de %s' % instance.sender.fullName ()})
        plaintext = get_template('email/message.txt')
        htmly = get_template('email/message.html')
        to = instance.receiver.email
        subject = 'Nuevo mensaje de %s' % instance.sender.fullName()
        from_email = 'agroceres@aramakao.com'
        text_content = plaintext.render(d)
        html_content = htmly.render(d)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception as e:
        print e
        pass
