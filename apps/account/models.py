#-*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from apps.extras.models import City,Occupation
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.timesince import timesince
from django.core.urlresolvers import reverse

class UserManager(BaseUserManager,models.Manager):
    '''This manager allows to extend the user class to create users with restricted privileges'''
    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        '''This function allows you to create users'''
        email=self.normalize_email(email)
        user=self.model(username=username, email=email, is_active=True, is_staff=is_staff,
            is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        profile = Profile(user=user)
        profile.save()
        from apps.store.models import ShippingAddress
        address = ShippingAddress(user=user)
        address.save()
        return user

    def getFullName(self,user):
        '''This function returns the full name of a user'''
    	if not user.last_name or not user.first_name:
    		return user.username
    	else:
    		return user.first_name + ' ' + user.last_name

    def create_user(self, username, email, password=None, **extra_fields):
        '''This function allows you to create users without extra privileges'''
        return self._create_user(username, email, password, False, False, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        '''This function allows you to create users with superuser privileges '''
        return self._create_user(username, email, password, True, True, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """This class inherits from AbstractBaseUser and allows user management"""
    username=models.CharField(max_length=100, unique=True)
    email=models.EmailField()
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    avatar=models.ImageField(upload_to='users',default='users/user_avatar.jpg')
    objects=UserManager()

    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)

    USERNAME_FIELD='username'
    REQUIRED_FIELDS =['email']

    def get_short_name(self):
        '''This function return the short name of the user'''
        return self.username

    def get_absolute_url(self):
		return reverse('user_profile', kwargs={'slug':self.username})

    def fullName(self):
        '''This function returns the full name of a user'''
        if not self.last_name or not self.first_name:
    		return self.username
    	else:
    		return self.first_name + ' ' + self.last_name

    def get_full_name(self):
        '''This function returns the full name of a user'''
        if not self.last_name or not self.first_name:
    		return self.username
    	else:
    		return self.first_name + ' ' + self.last_name

class Profile(models.Model):
    '''This model allows the user to add a user profile'''
    user=models.OneToOneField(User)
    occupation=models.ForeignKey(Occupation,blank=True, null=True)
    birth_day=models.DateField(default=timezone.now)
    gender=models.CharField(max_length=1,choices=(('M', 'Masculino'), ('F', 'Femenino')))
    phone=models.CharField(max_length=20, blank=True, null=True)
    mobile=models.CharField(max_length=20, blank=True, null=True)
    address=models.CharField(max_length=100, blank=True, null=True)
    twitter=models.CharField(max_length=100, blank=True, null=True)
    facebook=models.CharField(max_length=100, blank=True, null=True)
    description=models.TextField(max_length=200, blank=True, null=True)
    banner=models.ImageField(upload_to='users_banners',default='users_banners/user_banner.jpg')

    def __unicode__(self):
        return self.user.username

    def get_occupation(self):
        '''This function returns the occupation if any'''
        try:
            return self.occupation.name
        except Exception as e:
            return 'Desconocida'

    def get_phone(self):
        '''This function returns the number phone if any'''
    	if self.phone:
    		return self.phone
    	else:
    		return 'No disponible'

    def get_farm(self):
        '''This function returns the farm if user have a farm'''
        from apps.farm.models import Farm
        try:
            farm = Farm.objects.get(user=self.user)
        except Farm.DoesNotExist:
            farm = Farm()
        return farm

    def get_states(self):
        '''This function returns the last ten status from user'''
        states=StateUser.objects.filter(user=self.user).order_by('-date')[:10]
        return states

class LoggedInMixin(object):
    '''This class checks whether the user is authenticated'''

    @classmethod
    def as_view(cls, **initkwargs):
        '''This function allows it to be used in generic views'''
        view = super(LoggedInMixin, cls).as_view(**initkwargs)
        return login_required(view)


class FriendManager(models.Manager):
    '''This manager can handle the class Friend to extend its functionality'''

    def getAllFriends(self,user):
        '''This functions returns all friends from a user'''
        friends = self.filter(user=user)
        for friend in friends:
            setattr(friend,'full_name',User.objects.getFullName(friend.friend))
        return friends

class Friend(models.Model):
    '''This model allows to handel friends'''
    user = models.ForeignKey(User,related_name="friend_user")
    friend = models.ForeignKey(User,related_name="friend_friend")
    date = models.DateTimeField(auto_now_add=True)
    objects = FriendManager()

    class Meta:
        unique_together=(('user','friend'),)

    def __unicode__(self):
        return self.user.username

    def date_since(self):
        '''This function returns the date that a user is a friend'''
        return "Amigos desde hace "+ timesince(self.date)

class InivitationFriend(models.Model):
    '''This model allows to handel friend requests'''
    user = models.ForeignKey(User,related_name="invitation_friend_user")
    friend = models.ForeignKey(User,related_name="invitation_friend_friend")
    comment = models.TextField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=(('user','friend'),)
    def __unicode__(self):
        return self.user.username

class StateUser(models.Model):
    '''This model allows to the user publish status'''
    user = models.ForeignKey(User)
    text = models.TextField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to='states_img',blank=True)

    def __unicode__(self):
        return self.text

    def count_comments(self):
        '''This function count the number of comments'''
        count = StateUserComment.objects.filter(state=self).count()
        return count

    def date_since(self):
        '''This function returns the publication date'''
	return "Publicado hace "+ timesince(self.date)

class StateUserComment(models.Model):
    '''This class allows comments a state'''
    user = models.ForeignKey(User)
    state = models.ForeignKey(StateUser)
    text = models.CharField(max_length=200)
    hearts = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    picture = models.ImageField(upload_to='states_img',blank=True)

    def __unicode__(self):
        return self.text

    def date_post(self):
        '''This function returns the publication date'''
        return "Hace "+ timesince(self.date)

class StateUserLike(models.Model):
    '''This class allows bookmark a state'''
    user = models.ForeignKey(User)
    state = models.ForeignKey(StateUser)

    class Meta:
        unique_together=(('user','state'),)

    def __unicode__(self):
        return self.user.username

def getStateUser(user):
    '''This function returns a state from a user'''
    if user.is_authenticated:
        status = StateUser.objects.filter(user=user).order_by('-date')
        for state in  status:
            count_comments = StateUserComment.objects.filter(state=state).count()
            count_likes = StateUserLike.objects.filter(user=user,state=state).count()
            setattr(state,'count_likes', count_likes)
            setattr(state,'count_comments', count_comments)
            setattr(state,'date_post', timesince(state.date))
        return status
    else:
        return 0

def getUserFullName(user):
    '''This function returns the full name from a user'''
    if not user.last_name or not user.first_name:
	return user.username
    else:
	return user.first_name + ' ' + user.last_name

def is_session(session_key):
    '''This function checks if a user is authenticated'''
    from django.contrib.auth import SESSION_KEY
    from django.contrib.sessions.models import Session
    try:
        session = Session.objects.get(session_key=session_key)
        session.get_decoded()[SESSION_KEY]
        return True
    except (Session.DoesNotExist, KeyError):
        return False

def remove_session(session_key):
    '''This function delete the user's session'''
    from django.contrib.auth import SESSION_KEY
    from django.contrib.sessions.models import Session
    try:
        session = Session.objects.get(session_key=session_key)
        session.delete()
        return True
    except (Session.DoesNotExist, KeyError):
        return False
