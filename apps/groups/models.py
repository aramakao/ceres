#-*- encoding: utf-8 -*-
from django.db import models
from apps.account.models import User, Profile, getUserFullName
from autoslug import AutoSlugField
from django.utils.timesince import timesince
from django.http import Http404
from django.core.urlresolvers import reverse

class GroupManager(models.Manager):
    '''This class allows manager the group model'''
    def isMemberGroup(self,user,group):
        try:
            isMember=GroupMember.objects.get(user=user,group=group)
            return True
        except GroupMember.DoesNotExist:
            return False

class Group(models.Model):
    '''This model allows save groups'''
    administrator = models.ForeignKey(User)
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='group_profile', default='group_profile/group_logo.jpg')
    slug = AutoSlugField(populate_from='name', unique_with='name', always_update=True)
    openning_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    phone = models.CharField(max_length=20,blank=True)
    address = models.CharField(max_length=30,blank=True)
    objects = GroupManager()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
		return reverse('group_profile', kwargs={'group':self.slug})

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Group,self).save(*args, **kwargs)
            profile = GroupProfile(group=self)
            member = GroupMember(group=self, user=self.administrator)
            member.save()
            profile.save()
        else:
            super(Group,self).save(*args, **kwargs)
        return self

    def getProducts(self):
        '''This function returns the products that a group have'''
        from apps.product.models import ProductsGroup, Product
        group_products = ProductsGroup.objects.filter(group=self)
        products=[]
        for pro in group_products:
            if pro.product.is_active:
                products.append(Product.objects.get(id=pro.product.id))
        return products

    def count_members(self):
        '''This function counts the members at group'''
        count = GroupMember.objects.filter(group=self).count()
        return count


class GroupProfile(models.Model):
    '''This model allows update infromation about the group'''
    group = models.OneToOneField(Group)
    slogan = models.CharField(blank=True, max_length=200, null=True)
    banner = models.ImageField(upload_to='group_profile', default='group_profile/group_banner.jpg')
    latitude = models.FloatField(null=True, blank=True, default=1.63789)
    longitude = models.FloatField(null=True, blank=True, default=-77.7452081)
    location = models.CharField(blank=True,max_length=200,null=True)
    location_slug = AutoSlugField(populate_from='location', always_update=True)

    def __unicode__(self):
        return self.group.name

    def get_slogan(self):
        '''This function returns the group's slogan'''
        slogan = self.slogan
        if not slogan:
            slogan = "Desconocido"
        return slogan

    def getImageMeta(self):
        return "/media/{0}".format(self.banner)

class GroupMember(models.Model):
    '''This models allows add members to the group'''
    group = models.ForeignKey(Group)
    user = models.ForeignKey(User)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=(('group','user'),)

    def __unicode__(self):
        return self.user.username

    def date_since(self):
        '''this function returns the joining date'''
        return "Se unió hace "+ timesince(self.date_joined)

class StateGroup(models.Model):
    '''this models allows publish status'''
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    text = models.TextField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to='states_img',blank=True)

    def __unicode__(self):
        return self.text

class InivitationGroup(models.Model):
    '''This model allows managing the invitation requests'''
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    comment = models.TextField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=(('group','user'),)
    def __unicode__(self):
        return self.user.username

class StateGroupComment(models.Model):
    '''This model allows comment a group state'''
    user = models.ForeignKey(User)
    state = models.ForeignKey(StateGroup)
    text = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to='states_img',blank=True)

    def __unicode__(self):
        return self.text

def getStateGroup(group):
    '''This function return the status by group'''
    status = StateGroup.objects.filter(group=group).order_by('-date')
    for state in  status:
        count_comments = StateGroupComment.objects.filter(state=state).count()
        setattr(state,'count_comments', count_comments)
        setattr(state,'date_post', timesince(state.date))
        setattr(state,'full_name', getUserFullName(state.user))
        setattr(state,'user_profile', Profile.objects.get(user=state.user))
    return status

def getMembersGroup(group):
    '''This function returns the members by group'''
    members = GroupMember.objects.filter(group=group)
    members_profile=[]
    for member in members:
        obj = Profile.objects.get(user=member.user)
        obj.member = member.id
        obj.user_name=getUserFullName(obj.user)
        obj.joined= member.date_joined
        obj.admin = isAdministratorGroup(member.user,member.group)
        members_profile.append(obj)
    return members_profile

def getIvitationsGroup(group):
    '''This function lists the inivitations by group'''
    inivitations = InivitationGroup.objects.filter(group=group)
    for inivitation in inivitations:
        inivitation.user_name = getUserFullName(inivitation.user)
    return inivitations

def isAdministratorGroup(user,group):
    '''This function checks if an user is gruop administrator'''
    if group.administrator == user:
        return True
    else:
        return False

def isMemberGroup(user,group):
    '''This function checks if an user is member of it'''
    try:
        isMember=GroupMember.objects.get(user=user,group=group)
        return True
    except GroupMember.DoesNotExist:
        raise Http404

def isMemberGroupView(user,group):
    '''This function checks if an user is member of it'''
    try:
        if user.is_authenticated():
            isMember=GroupMember.objects.get(user=user,group=group)
            return True
        else:
            return False
    except GroupMember.DoesNotExist:
        return False

def acceptInvitation(invitation):
    '''This function allows accept an invitation'''
    invitation = InivitationGroup.objects.get(id=invitation)
    member = GroupMember(group=invitation.group,user=invitation.user)
    member.save()
    invitation.delete()
    return member

def rejectInvitation(invitation):
    '''This function reject an invitation'''
    invitation = InivitationGroup.objects.get(id=invitation)
    user = invitation.user
    invitation.delete()
    return user
