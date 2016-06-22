#-*- encoding: utf-8 -*-
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, UpdateView, FormView, ListView
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q
from .forms import *
from apps.account.models import LoggedInMixin
from apps.message.models import Message
from apps.message.forms import MessageForm
from django.contrib.auth import authenticate,login
from django.contrib.auth import update_session_auth_hash
from .models import *
from apps.ceres.processors import getUserFullName, getFarmAdmin, getActiveGroupsUser
from apps.ceres.notification import notificationComment, notificationFriendInvitation
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.utils.timesince import timesince
from notifications.models import Notification
from django.http import Http404
import json

def Login(request):
    '''This function allows the login, checks if the username and password are right'''
    if request.method=='POST':
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            username=request.POST['username']
            password=request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if request.user.is_authenticated():
                    request.session.set_expiry(60000)
                if request.POST.has_key('remember_me'):
                    request.session.set_expiry(1209600)
                if 'next' in request.GET:
                    return redirect(request.POST.get('next',request.GET['next']))
                else:
                    return redirect('home')
            else:
                messages.error(request, 'Usuario y/o Contraseña Incorrecta')
        else:
            messages.error(request, 'Tenemos un problema')
    else:
        login_form=LoginForm()
    return render(request,'account/login.html',{'login_form':login_form})

def Register(request):
    '''This functions allosws the register for new users'''
    if request.method == "POST":
        user_register = UserRegisterForm(request.POST)
        if user_register.is_valid():
            username = user_register.cleaned_data['username']
            email = user_register.cleaned_data['email']
            password = user_register.cleaned_data['password']
            re_password = request.POST['re_password']
            if re_password==password:
                User.objects.create_user(username,email,password)
                user= authenticate(username=username,password=password)
                login(request,user)
                return redirect('mi_agro')
            else:
                messages.error(request, 'Las contraseñas no coinciden!')
        else:
            for err in user_register.errors:
                if err=='username':
                    messages.error(request, 'Ya existe ese nombre de usuario')
                else:
                    messages.error(request, 'Tenemos un problema')
    else:
        user_register=UserRegisterForm()
    return render(request,'account/register.html',{'user_register':user_register})

def reset_confirm(request, uidb64=None, token=None):
    '''This function return after the user request reset the password'''
    return password_reset_confirm(request, template_name='account/password_reset_confirm.html',
        uidb64=uidb64,
        token=token,
        post_reset_redirect=reverse('login'))

def Reset(request):
    '''This function allows reset the password, it return a form with the email address and send
    an email with an url token for reset the password'''
    if request.method=='POST':
        reset_form=ResetPasswordForm(request.POST)
        if reset_form.is_valid():
            email=reset_form.cleaned_data['email']
            if User.objects.filter(email=email):
                return password_reset(request, template_name='account/reset.html',
                email_template_name='account/reset_email.html',
                is_admin_site=False,
                html_email_template_name='account/reset_email.html',
                subject_template_name='account/reset_subject.txt',
                post_reset_redirect=reverse('account:forget_succes'))
            else:
                messages.error(request, 'La dirección de Correo Electrónico no existe')
        else:
            messages.error(request, 'Tenemos un problema!')
    else:
        reset_form=ResetPasswordForm()
    return render(request,'account/reset.html',{'reset_form':reset_form})

class ForgetSucces(TemplateView):
    '''This class returns a template after the request for reset the password is success'''
    template_name='account/password_reset_done.html'

class UpdateProfileView(LoggedInMixin,TemplateView):
    '''This class allows update the user profile'''
    template_name='account/profile_edit.html'

    def get_context_data(self,**kwargs):
        '''This functions return the user form and the profile form'''
        context = super(UpdateProfileView, self).get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user)
        profile = Profile.objects.get(user=user)
        context['form_user']=UserForm(self.request.POST or None, instance = user)
        context['form_profile']=ProfileForm(self.request.POST or None, instance=profile)
        return context

    def post(self,request,*args,**kwargs):
        '''This funtion save the forms and update the user and user profile'''
        try:
            context = self.get_context_data()
            if context["form_user"].is_valid() and context["form_profile"].is_valid():
                context["form_user"].save()
                context["form_profile"].save()
                messages.success(self.request, 'Tu información se ha actualizado correctamente!')
            else:
                messages.error(self.request, 'Por favor revisa tu información!')
            return HttpResponseRedirect(reverse_lazy('profile'))
        except Exception as e:
            messages.error(self.request, 'Tenemos un problema en el servidor!')
            return HttpResponseRedirect(reverse_lazy('profile'))

class UpdatePasswordView(LoggedInMixin,FormView):
    form_class=UpdatePasswordForm
    template_name =  'account/update_password.html'
    success_url = reverse_lazy('update_password')

    def form_valid(self, form):
        if self.request.method=='POST':
            newpassword=form.cleaned_data['new_password1']
            username=self.request.user.username
            password=form.cleaned_data['old_password']

            user = authenticate(username=username, password=password)
            if user is not None:
                user.set_password(newpassword)
                user.save()
                update_session_auth_hash(self.request, self.request.user)
                messages.success(self.request, 'Contraseña actualizada correctamente!')
            else:
                messages.error(self.request, 'La contraseña actual no es correcta')

        return super(UpdatePasswordView, self).form_valid(form)

class ProfileView(TemplateView):
    '''This class allows view a profile'''
    template_name = 'account/profile.html'

    def get_context_data(self,**kwargs):
        '''This function returns user profile, farms, groups, friends, status from an user'''
        try:
            context = super(ProfileView, self).get_context_data(**kwargs)
            user_profile=get_object_or_404(User, username = self.kwargs['slug'])
            if user_profile == self.request.user:
                if 'state' in self.request.GET:
                    notifications=Notification.objects.get(id=self.request.GET['state'])
                    notifications.mark_as_read()
            context['profile'] = get_object_or_404(Profile, user = user_profile)
            context['profile_name'] = getUserFullName(user_profile)
            context['farm'] = getFarmAdmin(user_profile)
            context['message_form'] = MessageForm
            context['groups'] = getActiveGroupsUser(user_profile)
            context['friends'] = Friend.objects.getAllFriends(user_profile)[:10]
            paginator = Paginator(getStateUser(user_profile),10)
            context['status']=paginator.page(1)
            if 'page' in self.request.GET:
                page = self.request.GET.get('page')
                try:
                    context['status'] = paginator.page(page)
                except PageNotAnInteger:
                    context['status'] = paginator.page(1)
                except EmptyPage:
                    context['status'] = paginator.page(paginator.num_pages)
            context['admin']=False
            context['comments_form'] = StateUserCommentForm()
            context['invitation_form'] = InivitationFriendForm()
            return context
        except Exception as e:
            print e
            raise


    def post(self, request, *args, **kwargs):
        '''This function allows send comments, invitations, messages'''
        if 'btn_comments' in request.POST:
            text = request.POST['text']
            state = request.POST['state']
            comment = StateUser.objects.get(id=state)
            if 'picture' in request.FILES:
                state = StateUserComment(state_id=state,user=request.user,text=text,picture=request.FILES['picture'])
            else:
                state = StateUserComment(state_id=state,user=request.user,text=text)
            state.save()
            notificationComment(request.user,comment.user,comment)
            messages.success(self.request, 'Publicación exitosa!')
        if 'btn_invitation' in request.POST:
            try:
                comment = request.POST['comment']
                user = User.objects.get(username=kwargs['slug'])
                invitation = InivitationFriend(friend=request.user,comment=comment,user=user)
                invitation.save()
                notificationFriendInvitation(request.user,user)
                messages.success(self.request, 'Invitación enviada correctamente!')
            except:
                messages.error(self.request, 'Ya la has enviado una solicitud de amistad!')
        if 'btn_message' in request.POST:
            form = MessageForm(request.POST)
            if form.is_valid():
                message_content=form.cleaned_data['message']
                receiver = User.objects.get(username=kwargs['slug'])
                if 'file' in request.FILES:
                    file = request.FILES['file']
                    message = Message(message=message_content,file=file,sender=request.user,receiver=receiver)
                else:
                    message = Message(message=message_content,sender=request.user,receiver=receiver)
                message.save()
                messages.success(self.request, 'Mensaje enviado correctamente!')
        return redirect('user_profile',slug=kwargs['slug'])

class NotificationsView(LoggedInMixin,ListView):
    '''This class list all notifications that the user has received'''
    template_name='account/notifications.html'
    paginate_by = 10
    context_object_name= 'notifications'

    def get_queryset(self):
        object_list=self.request.user.notifications.all()
        return object_list

class MyFriendList(LoggedInMixin,ListView):
    '''This class list all friends of the user'''
    template_name = 'account/my_friends.html'
    paginate_by = 10
    context_object_name = 'friends'

    def get_queryset(self):
        '''This function filters friends by user logged'''
        object_list = Friend.objects.getAllFriends(user=self.request.user)
        return object_list

    def get_context_data(self,**kwargs):
        '''This function returns a form for delete a friend'''
        context = super(MyFriendList,self).get_context_data(**kwargs)
        context['friend_form'] = FriendDeleteForm()
        return context

    def post(self,request,*args,**kwargs):
        '''This function allows delete a friend'''
        friend_id = request.POST['user']
        friend = isFriend(request.user,friend_id)
        user = Friend.objects.get(user=friend.friend,friend=request.user)
        friend.delete()
        user.delete()
        messages.success(self.request, 'Borrado de la lista de amigos!')
        return HttpResponseRedirect(reverse('my_friends'))

class FriendInvitationList(LoggedInMixin,ListView):
    '''This class lists all friend requests'''
    template_name = 'account/friends_invitation.html'
    paginate_by = 10
    context_object_name = 'invitations'

    def get_queryset(self):
        '''This class lists all friend requests by user logged'''
        object_list = InivitationFriend.objects.filter(user=self.request.user)
        return object_list

    def get_context_data(self,**kwargs):
        '''This function mark as read a notification'''
        context = super(FriendInvitationList,self).get_context_data(**kwargs)
        if 'state' in self.request.GET:
            notifications=Notification.objects.get(id=self.request.GET['state'])
            notifications.mark_as_read()
        return context

    def post(self,request,*args,**kwargs):
        '''This function allows accept,reject friend requests'''
        for key in request.POST:
            if key.startswith('accept:'):
                accept = key[7:]
                invitation = isInvitation(request.user,accept)
                friend = Friend(user=invitation.user,friend=invitation.friend)
                user = Friend(friend=invitation.user,user=invitation.friend)
                inivitations = InivitationFriend.objects.filter(Q(user=invitation.user,friend=invitation.friend)|Q(friend=invitation.user,user=invitation.friend))
                friend.save()
                user.save()
                invitation.delete()
                inivitations.delete()
                messages.success(self.request, 'Amistad aceptada!')
                break
            if key.startswith('reject:'):
                reject = key[7:]
                invitation = isInvitation(request.user,reject)
                invitation.delete()
                messages.success(self.request, 'Amistad rechazada!')
                break
        return HttpResponseRedirect(reverse('friends_invitations'))

def isFriend(user,friend_id):
    '''This function checks if an user is friend'''
    try:
        friend = Friend.objects.get(id=friend_id)
        if friend.user == user:
            return friend
        else:
            raise Http404
    except Friend.DoesNotExist:
        raise Http404

def isInvitation(user,invitation_id):
    '''This function checks if an user and he sent him a friend request'''
    try:
        inivitation = InivitationFriend.objects.get(id=invitation_id)
        if inivitation.user == user:
            return inivitation
        else:
            raise Http404
    except InivitationFriend.DoesNotExist:
        raise Http404

def changePictureProfile(request):
    '''This function allows change the picture profile a user'''
    if request.is_ajax():
        user=User.objects.get(username=request.user)
        user.avatar=request.FILES['file_upload']
        user.save()
        return HttpResponse(user.avatar.url, content_type="text/plain")
    else:
        raise Http404

def changePictureBanner(request):
    '''This function allows change the banner profile a user'''
    if request.is_ajax():
        profile=Profile.objects.get(user__username=request.user)
        profile.banner=request.FILES['file_upload']
        profile.save()
        return HttpResponse(profile.banner.url, content_type="text/plain")
    else:
        raise Http404
