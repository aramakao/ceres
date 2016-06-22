from django.shortcuts import render, get_object_or_404, redirect
from apps.account.models import LoggedInMixin
from django.contrib import messages
from django.views.generic import ListView, TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from .forms import *
from .tasks import *

class ConversationsList(LoggedInMixin,ListView):
    '''This view lists the messages group by sender and receiver'''
    template_name = 'message/conversations.html'
    paginate_by = 10
    context_object_name = 'conversations'

    def get_queryset(self):
        '''This function filters by user'''
        object_list = Message.objects.getConversations(self.request.user)
        return object_list

class MessagesList(LoggedInMixin,TemplateView):
    '''This view lists the messages from sender'''
    template_name = 'message/messages.html'

    def get_context_data(self,**kwargs):
        '''This function helps to paginate de messages'''
        context = super(MessagesList,self).get_context_data(**kwargs)
        sender = get_object_or_404(User,username=self.kwargs['username'])
        Message.objects.updateRead(self.request.user,sender)
        context['sender'] = sender
        paginator = Paginator(Message.objects.getMessages(self.request.user,sender),10)
        context['my_messages']=paginator.page(1)
        if 'page' in self.request.GET:
            page = self.request.GET.get('page')
            try:
                context['my_messages'] = paginator.page(page)
            except PageNotAnInteger:
                context['my_messages'] = paginator.page(1)
            except EmptyPage:
                context['my_messages'] = paginator.page(paginator.num_pages)
        context['message_form'] = MessageForm()
        return context

    def post(self,request,*args,**kwargs):
        '''This function saves a message'''
        form = MessageForm(request.POST)
        if form.is_valid():
            message_content=form.cleaned_data['message']
            receiver = User.objects.get(username=kwargs['username'])
            if 'file' in request.FILES:
                file = request.FILES['file']
                message = Message(sender=request.user,receiver=receiver,message=message_content,file=file)
            else:
                message = Message(sender=request.user,receiver=receiver,message=message_content)
            message.save()
            messages.success(self.request, 'Mensaje enviado correctamente!')
        return redirect('message_app:message',username=kwargs['username'])
