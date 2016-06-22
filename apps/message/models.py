from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timesince import timesince
from apps.account.models import User
from apps.groups.models import Group
from django.db.models import Q
import os

class MessageManager(models.Manager):
    '''This manager allows extends the message model'''

    def getConversations(self,user):
        '''This function group all messages by sender and receiver'''
        messages = Message.objects.filter(Q(sender=user)|Q(receiver=user)).order_by('-date')
        conversations = []
        seen = set()
        for message in messages:
            setattr(message,'timesince',timesince(message.date))
            if message.sender == user:
                receiver = message.sender
                message.sender = message.receiver
                message.receiver = receiver
                setattr(message,'icon','fa fa-reply')
            else:
                setattr(message,'icon','fa fa-inbox')
            if message.sender not in seen:
                conversations.append(message)
                seen.add(message.sender)
        return conversations

    def getMessages(self,user,sender):
        '''This function list the messages from sender and receiver'''
        messages = Message.objects.filter(Q(sender=user,receiver=sender)|Q(receiver=user,sender=sender)).order_by('-date')
        conversations = []
        for message in messages:
            setattr(message,'timesince',timesince(message.date))
            if message.sender == user:
                receiver = message.sender
                message.sender = message.receiver
                message.receiver = receiver
                setattr(message,'is_receiver',True)
            else:
                setattr(message,'is_receiver',False)
            filename = Message.objects.filename(message)

            if filename:
                setattr(message,'filename',Message.objects.filename(message))
            conversations.append(message)
        return conversations

    def filename(self,message):
        '''This function returns the path from a file'''
        return os.path.basename(message.file.name)

    def countUnread(self,receiver):
        '''This function counts unread messages'''
        count = Message.objects.filter(receiver=receiver,is_read=False).count()
        return count

    def updateRead(self,user,sender):
        '''this function update the state read from message'''
        Message.objects.filter(receiver=user,sender=sender).update(is_read=True)
        return True

class Message(models.Model):
    '''This model allows create messages'''
    sender = models.ForeignKey(User,related_name='sender_message')
    receiver = models.ForeignKey(User,related_name='receiver_message')
    date = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=200)
    file = models.FileField(upload_to='messages', null=True, blank=True)
    is_read = models.BooleanField(default=False)
    objects = MessageManager()

    def __unicode__(self):
        return self.sender.username

class MessageGroupManager(models.Manager):
    '''This manager allows extends the message model'''
    def getMessages(self,group):
        '''This function lists the messages by group'''
        messages = MessageGroup.objects.filter(group=group).order_by('-date')
        for message in messages:
            setattr(message,'full_name',User.objects.getFullName(message.user))
        return messages

class MessageGroup(models.Model):
    '''This model allows create messages'''
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    date = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=200)
    file = models.FileField(upload_to='messages', null=True, blank=True)
    objects = MessageGroupManager()

    def save(self):
        if Group.objects.isMemberGroup(self.user,self.group):
            super(MessageGroup, self).save()
        else:
            raise ValidationError('Error')

    def __unicode__(self):
        return self.user.username

    def filename(self):
        '''This function return the file path'''
        return os.path.basename(self.file.name)
