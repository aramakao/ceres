#-*- encoding: utf-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView,CreateView, ListView, UpdateView
from django.core.urlresolvers import reverse_lazy, reverse
from apps.account.models import LoggedInMixin, Profile
from apps.product.models import Product, ProductsGroup, haveProductsFarm, ProductsGroup
from apps.ceres.processors import getUserFullName
from apps.message.models import MessageGroup, Message
from apps.message.forms import MessageGroupForm, MessageForm
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from notifications.models import Notification
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from .forms import *
from .models import *
from apps.ceres.notification import *

class GroupsView(ListView):
    '''Thsi view list all groups'''
    model = GroupProfile
    template_name = 'groups/groups.html'
    paginate_by = 20
    context_object_name = 'groups'

    def get_queryset(self):
        '''This function filters active groups'''
        object_list = self.model.objects.filter(group__is_active=True).order_by('group')
        return object_list

class GroupProfileView(TemplateView):
    '''This view allows view a group'''
    template_name = 'groups/group.html'

    def get_context_data(self,**kwargs):
        '''This function return members,status,products, invitation form and message form'''
        context = super(GroupProfileView,self).get_context_data(**kwargs)
        group = get_object_or_404(Group,slug=self.kwargs['group'])
        if group.is_active:
            context['is_member']=isMemberGroupView(user=self.request.user,group=group)
            context['group']=get_object_or_404(GroupProfile,group=group)
            context['members']=getMembersGroup(group)
            context['invitation_form']=InivitationGroupForm()
            context['message_form']=MessageForm()
            paginator = Paginator(getStateGroup(group),10)
            context['status']=paginator.page(1)
            if 'page' in self.request.GET:
                page = self.request.GET.get('page')
                try:
                    context['status'] = paginator.page(page)
                except PageNotAnInteger:
                    context['status'] = paginator.page(1)
                except EmptyPage:
                    context['status'] = paginator.page(paginator.num_pages)
            context['comments_form'] = StateGroupCommentForm()
            products = ProductsGroup.objects.filter(group=group,product__is_active=True)
            context['products_group']=products
            return context
        else:
            raise Http404

    def post(self,request,*args,**kwargs):
        '''This function allows publish comments, send invitation and messages to the group'''
        slug = kwargs['group']
        group = Group.objects.get(slug=slug)
        if 'btn_comments' in request.POST:
            text = request.POST['text']
            state = request.POST['state']
            if 'picture' in request.FILES:
                state = StateGroupComment(state_id=state,user=request.user,text=text,picture=request.FILES['picture'])
            else:
                state = StateGroupComment(state_id=state,user=request.user,text=text)
            state.save()
            notificationCommentGroup(request.user,group,group)
            messages.success(self.request, 'Publicación exitosa!')
        if 'btn_invitation' in request.POST:
            try:
                comment = request.POST['comment']
                inivitation = InivitationGroup(comment=comment,group=group,user=request.user)
                inivitation.save()
                notificationInvitationGroup(request.user,group,group)
                messages.success(self.request, 'Invitación enviada!')
            except IntegrityError:
                messages.error(self.request, 'Ya has enviado una invitación a este grupo!')
        if 'btn_messages' in request.POST:
            comment = request.POST['message']
            if 'file' in request.FILES:
                message = Message(sender=request.user,receiver=group.administrator,file=request.FILE['file'],message=comment)
            else:
                message = Message(sender=request.user,receiver=group.administrator,message=comment)
            message.save(sender=request.user,receiver=group.administrator)
            messages.success(self.request, 'Se ha enviado el mensaje al administrador del grupo!')
        return HttpResponseRedirect(reverse('group_profile', kwargs={'group':slug}))

class RegisterGroup(LoggedInMixin,CreateView):
    '''This view allows create a new group'''
    template_name = 'groups/register.html'
    model = Group
    form_class = GroupForm

    def post(self,request,*args,**kwargs):
        '''This function checks if the form is valid and save it'''
        groupForm=GroupForm(request.POST)
        if groupForm.is_valid():
            name = groupForm.cleaned_data['name']
            phone = groupForm.cleaned_data['phone']
            address = groupForm.cleaned_data['address']
            group = Group(name= name, phone=phone, address=address, administrator= request.user).save()
            messages.success(self.request, 'Grupo creado!')
            return HttpResponseRedirect(reverse('groups_app:my_group', kwargs={'slug':group.slug}))
        else:
            messages.error(self.request, 'Por favor verifique la información!')
            return HttpResponseRedirect(reverse('groups_app:register'))

class MyGroupView(LoggedInMixin,TemplateView):
    '''This view return the landing page of the group'''
    template_name = 'groups/my_group.html'

    def get_context_data(self,**kwargs):
        '''This function return members, messages, invitations, comments, products'''
        context = super(MyGroupView,self).get_context_data(**kwargs)
        group = get_object_or_404(Group,slug=self.kwargs['slug'])
        if isMemberGroup(self.request.user,group):
            if 'state' in self.request.GET:
                notifications=Notification.objects.get(id=self.request.GET['state'])
                notifications.mark_as_read()
            context['group'] = get_object_or_404(GroupProfile,group=group)
            context['messages_group_form'] = MessageGroupForm()
            context['members'] = getMembersGroup(group)
            paginator_message =Paginator(MessageGroup.objects.getMessages(group),10)
            context['messages_group'] = paginator_message.page(1)
            if 'page_messages' in self.request.GET:
                page_messages = self.request.GET.get('page_messages')
                try:
                    context['messages_group'] = paginator_message.page(page_messages)
                except PageNotAnInteger:
                    context['messages_group'] = paginator_message.page(1)
                except EmptyPage:
                    context['messages_group'] = paginator_message.page(paginator_message.num_pages)
            context['inivitations'] = getIvitationsGroup(group)
            context['admin'] = isAdministratorGroup(self.request.user,group)
            context['haveProducts']=haveProductsFarm(self.request.user)
            context['state_form'] = StateGroupForm()
            context['comments_form'] = StateGroupCommentForm()
            paginator = Paginator(getStateGroup(group),10)
            context['status']=paginator.page(1)
            if 'page' in self.request.GET:
                page = self.request.GET.get('page')
                try:
                    context['status'] = paginator.page(page)
                except PageNotAnInteger:
                    context['status'] = paginator.page(1)
                except EmptyPage:
                    context['status'] = paginator.page(paginator.num_pages)
            products = ProductsGroup.objects.filter(group=group)
            context['products_group']=products

        return context

    def post(self,request,*args,**kwargs):
        '''This function allows publish and delete status, accept invitations, comments status'''
        slug = kwargs['slug']
        group = Group.objects.get(slug=slug)
        for key in request.POST:
            if key.startswith('btn_delete:'):
                delete =  key[11:]
                state=StateGroup.objects.get(id=delete)
                state.delete()
                messages.success(self.request, 'Publicación borrada!')
                break
            if key.startswith('accept_invitation:'):
                accept = key[18:]
                member = acceptInvitation(accept)
                messages.success(self.request, 'Felicidades tienes un nuevo integrante en tu asociación')
                notificationAcceptInvitationGroup(request.user,member.user,group)
                break
            if key.startswith('reject_invitation:'):
                reject = key[18:]
                member = rejectInvitation(reject)
                messages.success(self.request, 'Invitación rechazada!')
                break
        if 'btn_state' in request.POST:
            text = request.POST['text']
            if 'picture' in request.FILES:
                state = StateGroup(user=request.user,group=group,text=text,picture=request.FILES['picture'])
            else:
                state = StateGroup(user=request.user,group=group,text=text)
            state.save()
            notificationStateGroup(request.user,group,group)
            messages.success(self.request, 'Publicación exitosa!')
        if 'btn_comments' in request.POST:
            text = request.POST['text']
            state = request.POST['state']
            if 'picture' in request.FILES:
                state = StateGroupComment(state_id=state,user=request.user,text=text,picture=request.FILES['picture'])
            else:
                state = StateGroupComment(state_id=state,user=request.user,text=text)
            state.save()
            notificationCommentGroup(request.user,group,group)
            messages.success(self.request, 'Publicación exitosa!')
        if 'leaveGroup' in request.POST:
            leaveGroup(user=request.user,group=group)
            messages.success(self.request, 'Has abandonado la asociación!')
            return redirect('groups_app:my_groups')
        if 'btn_messages_group' in request.POST:
            comment = request.POST['message']
            if 'file' in request.FILES:
                message = MessageGroup(user=request.user,group=group,file=request.FILES['file'],message=comment)
            else:
                message = MessageGroup(user=request.user,group=group,message=comment)
            message.save()
            notificationMessageGroup(request.user,group,group)
            messages.success(self.request, 'Mensaje enviado exitosamente!')
        return HttpResponseRedirect(reverse('groups_app:my_group', kwargs={'slug':slug}))

class MyProductsGroupView(LoggedInMixin,TemplateView):
    '''This view list the products that a member have'''
    template_name = 'groups/my_products.html'

    def get_context_data(self,**kwargs):
        '''This function checks if a user is member and return the products'''
        context = super(MyProductsGroupView,self).get_context_data(**kwargs)
        group = get_object_or_404(Group,slug=self.kwargs['slug'])
        if isMemberGroup(self.request.user,group):
            if haveProductsFarm(self.request.user):
                context['group'] = get_object_or_404(GroupProfile,group=group)
                myProductsGroup = ProductsGroup.objects.filter(group=group,product__farm__user=self.request.user)
                myProducts = Product.objects.filter(farm__user=self.request.user,is_active=True)
                for m_product in myProducts:
                    for g in myProductsGroup:
                        if g.product==m_product:
                            setattr(m_product,'in_farm',True)
                            break
                        else:
                            setattr(m_product,'in_farm',False)
                context['my_products']=myProducts
            else:
                raise Http404
        else:
            raise Http404
        return context

class MembersGroup(LoggedInMixin,TemplateView):
    template_name = 'groups/members.html'

    def get_context_data(self,**kwargs):
        context = super(MembersGroup,self).get_context_data(**kwargs)
        group = get_object_or_404(Group,slug=self.kwargs['slug'])
        if isAdministratorGroup(self.request.user,group) == False:
            raise Http404
        else:
            context['group'] = get_object_or_404(GroupProfile,group=group)
            context['members'] = getMembersGroup(group)
        return context

    def post(self,request,*args,**kwargs):
        slug = kwargs['slug']
        group = Group.objects.get(slug=slug)
        for key in request.POST:
            if key.startswith('delete:'):
                delete =  key[7:]
                member = GroupMember.objects.get(id=delete)
                leaveGroup(user=member.user,group=member.group)
                messages.success(self.request, 'Participante retirado de la Asociación!')
        return HttpResponseRedirect(reverse('groups_app:members', kwargs={'slug':slug}))

class MyGroupsList(LoggedInMixin,ListView):
    '''This view returns the members'''
    model = GroupMember
    template_name = 'groups/my_groups_list.html'
    context_object_name = 'groups'

    def get_queryset(self):
        '''This function filters the members by group'''
        object_list = self.model.objects.filter(user=self.request.user).order_by('group')
        for obj in object_list:
            members=GroupMember.objects.filter(group=obj.group)
            groupProfile=GroupProfile.objects.get(group=obj.group)
            setattr(obj,'members',members.count)
            setattr(obj,'profile',groupProfile)
        return object_list

class MyGroupAdminView(LoggedInMixin,UpdateView):
    '''This view allows admin the group'''
    template_name = 'groups/group_admin.html'
    model = Group
    form_class = GroupForm
    success_url = reverse_lazy('groups_app:group_admin',kwargs={'slug': 'aso-cuyo'})

    def get_context_data(self,**kwargs):
        '''This function checks if the user is administrator'''
        context = super(MyGroupAdminView,self).get_context_data(**kwargs)
        group = get_object_or_404(Group,slug=self.kwargs['slug'])
        if isAdministratorGroup(self.request.user,group) == False:
            raise Http404
        context['group'] = get_object_or_404(GroupProfile,group=group)
        context['profile_form'] = GroupProfileForm(instance=GroupProfile.objects.get(group=group))
        return context

    def form_valid(self,form,**kwargs):
        '''This function checks if the form is valid before save it'''
        if self.request.method=='POST':
            messages.success(self.request,"Has actualizado {0} correctamente".format(self.request.POST['name']))
            group = get_object_or_404(Group,slug=self.kwargs['slug'])
            latitude=self.request.POST['latitude']
            longitude=self.request.POST['longitude']
            location=self.request.POST['location']
            slogan=self.request.POST['slogan']
            groupProfile=GroupProfile.objects.get(group=group)
            groupProfile.latitude=latitude
            groupProfile.longitude=longitude
            groupProfile.location=location
            groupProfile.slogan=slogan
            groupProfile.save()
        return super(MyGroupAdminView,self).form_valid(form)

    def get_success_url(self):
        group = Group.objects.get(name=self.request.POST['name'])
        return reverse_lazy('groups_app:group_admin',kwargs={'slug': group.slug})

def leaveGroup(user,group):
    '''This function allows leave a group'''
    if isMemberGroup(user,group):
        ProductsGroup.objects.filter(product__farm__user=user,group=group).delete()
        GroupMember.objects.get(user=user,group=group).delete()

def changePictureProfile(request):
    '''This function allows change the group logo'''
    if request.is_ajax():
        group=Group.objects.get(administrator=request.user,slug=request.POST['group'])
        group.logo=request.FILES['file_upload']
        group.save()
        return HttpResponse(group.logo.url, content_type="text/plain")
    else:
        raise Http404

def changePictureBanner(request):
    '''This function allows change the banner'''
    if request.is_ajax():
        group=GroupProfile.objects.get(group__slug=request.POST['group'])
        group.banner=request.FILES['file_upload']
        group.save()
        return HttpResponse(group.banner.url, content_type="text/plain")
    else:
        raise Http404
