#-*- encoding: utf-8 -*-
from notifications import notify
from apps.groups.models import *

def notificationShop(sender,receiver,target):
    notify.send(sender, recipient=receiver, verb='Ha realizado una compra en tu granja. N° Compra:',description='fa fa-shopping-cart', target=target)

def notificationAskProduct(sender,receiver,target):
    notify.send(sender, recipient=receiver, verb='Ha realizado una pregunta en tu producto %s' % target.product.name, description='fa fa-question-circle')

def notificationReplyProduct(sender,receiver,target):
    notify.send(sender, recipient=receiver, verb='Ha respondido tu pregunta sobre el producto %s' % target.product.name, description='fa fa-question-circle')

def notificationOrderBuyer(sender,receiver,target):
    notify.send(sender, recipient=receiver, verb='Tienes una notificacion en la orden de compra N°:',description='fa fa-flag', target=target)

def notificationOrderSeller(sender,receiver,target):
    notify.send(sender, recipient=receiver, verb='Tienes una notificacion en la orden de compra N°:',description='fa fa-flag-o', target=target)

def notificationComment(sender,receiver,target):
    if sender!=receiver:
        notify.send(sender, recipient=receiver, verb='Ha comentado tu publicación',description='fa fa-comments', target=target)

def notificationStateGroup(sender,group,target):
    members = GroupMember.objects.filter(group=group)
    for member in members:
        if sender!=member.user:
            notify.send(sender, recipient=member.user, verb='Ha publicado en tu grupo',description='fa fa-users', target=target)

def notificationCommentGroup(sender,group,target):
    members = GroupMember.objects.filter(group=group)
    for member in members:
        if sender!=member.user:
            notify.send(sender, recipient=member.user, verb='Ha comentado una publicación en tu grupo',description='fa fa-users', target=target)

def notificationMessageGroup(sender,group,target):
    members = GroupMember.objects.filter(group=group)
    for member in members:
        if sender!=member.user:
            notify.send(sender, recipient=member.user, verb='Ha dejado un mensaje en tu grupo',description='fa fa-users', target=target)

def notificationInvitationGroup(sender,group,target):
    members = GroupMember.objects.filter(group=group)
    for member in members:
        if sender!=member.user:
            notify.send(sender, recipient=member.user, verb='Ha enviado una solicitud para unirte a tu grupo',description='fa fa-users', target=target)

def notificationAcceptInvitationGroup(sender,receiver,target):
    notify.send(sender, recipient=receiver, verb='Te ha agreagado al grupo',description='fa fa-users', target=target)

def notificationFriendInvitation(sender,receiver):
    notify.send(sender, recipient=receiver, verb='Quiere ser tu amigo',description='fa fa-angellist')
