from django.core.mail import EmailMultiAlternatives

def sendeEmailNotification():
    subject, from_email, to = 'hello', 'hello@agroceres.net', 'jfajardo89@gmail.com'
    text_content = 'This is an important message.'
    html_content = '<p>This is an <strong>important</strong> message.</p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
