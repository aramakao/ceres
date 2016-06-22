#-*- encoding: utf-8 -*-
from django.shortcuts import render,get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, UpdateView, DetailView, CreateView, DeleteView
from django.http import HttpResponse, Http404, HttpResponseRedirect
from apps.product.models import Product
from apps.farm.models import FarmProfile,Farm
from apps.account.models import Profile, StateUser, StateUserComment
from apps.groups.models import GroupProfile
from django.contrib import messages
from django.db import IntegrityError
from datetime import datetime
from .models import *
from .forms import *
from decimal import *
from notifications.models import Notification
from django.db.models import Q
from apps.account.models import LoggedInMixin
from django.core.urlresolvers import reverse_lazy, reverse
from apps.product.models import ProductCategory
from apps.blog.models import Blog
from django.db.models import Count, Sum
from apps.account.forms import StateUserCommentForm
from apps.ceres.notification import notificationOrderBuyer, notificationOrderSeller
from apps.ceres.processors import getUserFullName,haveFarm, getFarmUser
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives
from .tasks import *
import json

class AboutView(TemplateView):
	template_name = 'store/about.html'

class HomePageView(TemplateView):
	template_name='store/index.html'

	def get_context_data(self, **kwargs):
		context = super(HomePageView, self).get_context_data(**kwargs)
		context['latest_products']=Product.objects.filter(farm__is_active=True,is_active=True).order_by('-id')[:15]
		context['adverts'] = Blog.objects.getBanners()
		context['comments_form'] = StateUserCommentForm()
		context['entries']=Blog.objects.all().order_by('-posted')[:10]
		context['status']=StateUser.objects.all().order_by('-date')[:5]
		context['users']=Profile.objects.all().order_by('?')[:10]
		context['farms']=FarmProfile.objects.all().order_by('?')[:10]
		context['groups']=GroupProfile.objects.all().order_by('?')[:10]
		return context

	def post(self, request, *args, **kwargs):
		if 'btn_comments' in request.POST:
			text = request.POST['text']
			state = request.POST['state']
			if 'picture' in request.FILES:
				state = StateUserComment(state_id=state,user=request.user,text=text,picture=request.FILES['picture'])
			else:
				state = StateUserComment(state_id=state,user=request.user,text=text)
			state.save()
			messages.success(self.request, 'Publicación exitosa!')
		return redirect(reverse_lazy('home'))

class ProductView(TemplateView):
	template_name='store/product.html'

	def dispatch(self,request,*args,**kwargs):
		context=self.get_context_data()
		if request.method=='POST':
			ask_form = AskForm(request.POST)
			if ask_form.is_valid():
				ask=ask_form.cleaned_data['ask']
				buyer=request.user
				product=get_object_or_404(Product,slug=self.kwargs['slug'])
				link=ask_form.save(commit=False)
				link.ask=ask
				link.buyer=buyer
				link.product=product
				link.seller=product.farm.user
				link.save()
				messages.success(request, 'Muy pronto resivirá respuesta por parte del vendedor!')
		return super(ProductView,self).render_to_response(context)

	def get_context_data(self, **kwargs):
		ask_form = AskForm()
		product=get_object_or_404(Product,slug=self.kwargs['slug'])
		farm = FarmProfile.objects.get(farm=product.farm)
		if product.is_active and product.farm.is_active:
			context = super(ProductView, self).get_context_data(**kwargs)
			context['product']=product
			context['fbProducts'] = getFeedbackProduct(product)
			context['shippings']=ShippingOption.objects.filter(farm=product.farm).order_by('name')
			context['payments']=Payment.objects.filter(farm=product.farm).order_by('payment')
			farm=get_object_or_404(FarmProfile,farm=context['product'].farm)
			context['feedback']=FeedbackProduct.objects.filter(order__product=product)
			if farm.farm.is_active:
				context['farm']=farm
			else:
				raise Http404('farm deactive')
			context['ask_form']=ask_form
			context['comments']=ProductComments.objects.filter(product=product).order_by('-date_post_ask')
			context['latest_products']=Product.objects.filter(farm__is_active=True,is_active=True).order_by('?')[:15]
			return context
		else:
			raise Http404

class ProductList(ListView):
	model = Product
	template_name ='store/products.html'
	paginate_by = 20
	context_object_name = 'products'

	def get_queryset(self):
		object_list = Product.objects.filter(is_active=True).order_by('name')
		return object_list

class StatusList(ListView):
	model = StateUser
	template_name ='store/status.html'
	paginate_by = 5
	context_object_name = 'status'

	def get_context_data(self,**kwargs):
		context = super(StatusList,self).get_context_data(**kwargs)
		context['comments_form'] = StateUserCommentForm()
		return context

	def post(self, request, *args, **kwargs):
		if 'btn_comments' in request.POST:
			text = request.POST['text']
			state = request.POST['state']
			if 'picture' in request.FILES:
				state = StateUserComment(state_id=state,user=request.user,text=text,picture=request.FILES['picture'])
			else:
				state = StateUserComment(state_id=state,user=request.user,text=text)
			state.save()
			messages.success(self.request, 'Publicación exitosa!')
		return redirect(reverse_lazy('status'))

class CategoryProductsView(ListView):
	model = Product
	template_name='store/category.html'
	paginate_by=20
	context_object_name= 'products'

	def get_queryset(self):
		category=get_object_or_404(ProductCategory,slug=self.kwargs['slug'])
		object_list=self.model.objects.filter(category=category,farm__is_active=True,is_active=True)
		return object_list

	def get_context_data(self, **kwargs):
		category=get_object_or_404(ProductCategory,slug=self.kwargs['slug'])
		context = super(CategoryProductsView, self).get_context_data(**kwargs)
		context['category']=category
		return context

class CategoriesView(ListView):
	template_name='store/category_list.html'
	model = ProductCategory
	context_object_name = 'categories'
	queryset = ProductCategory.objects.all().order_by('name')

class ProductCommentsListView(LoggedInMixin,ListView):
	template_name='store/product_comments_list.html'
	paginate_by=5
	context_object_name='comments'

	def get_queryset(self):
		return ProductComments.objects.getComments(user=self.request.user)

	def post(self,request,*args,**kwargs):
		comment_id=request.POST['comment']
		reply=request.POST['reply']
		comment = ProductComments.objects.get(id=comment_id, seller=request.user)
		comment.reply=reply
		comment.is_read=True
		comment.date_post_reply=datetime.datetime.now()
		comment.save()
		messages.success(self.request, 'Pregunta respondida!')
		return HttpResponseRedirect(reverse('product_comment'))

	def get_context_data(self,**kwargs):
		context = super(ProductCommentsListView, self).get_context_data(**kwargs)
		if 'state' in self.request.GET:
			notifications=Notification.objects.get(id=self.request.GET['state'])
			notifications.mark_as_read()
		return context

class UpdateAskView(LoggedInMixin,UpdateView):
	model = ProductComments
	template_name = 'store/product_ask_reply.html'
	form_class= ReplyForm
	success_url = reverse_lazy('comments')

	def get_object(self,queryset=None):
		obj = super(UpdateAskView, self).get_object()
		if not obj.seller == self.request.user:
			raise Http404
		return obj

	def get_context_data(self, **kwargs):
	    context = super(UpdateAskView, self).get_context_data(**kwargs)
	    context['comment']=get_object_or_404(ProductComments,seller=self.request.user)
	    return context

	def form_valid(self,form):
		self.object=form.save(commit=False)
		self.object.is_read=True
		return super(UpdateAskView, self).form_valid(form)

class FarmView(TemplateView):
	template_name='store/farm.html'

	def get_context_data(self, **kwargs):
	    context = super(FarmView, self).get_context_data(**kwargs)
	    farm=get_object_or_404(Farm,slug=self.kwargs['farm'])
	    if farm.is_active:
		    context['farm']=get_object_or_404(FarmProfile,farm=farm)
		    context['farmer_name'] = getUserFullName(farm.user)
		    context['feedback']=getFeedbackFarm(farm)
		    context['farmer_profile']=get_object_or_404(Profile,user=farm.user)
		    context['categories']=Product.objects.filter(farm=farm,is_active=True).distinct('category')
		    context['latest_products']=Product.objects.filter(farm=farm,is_active=True)[:15]
		    return context
	    else:
			raise Http404

class ProductsFarmView(ListView):
	model = Product
	template_name='store/products_farm.html'
	paginate_by=20
	context_object_name= 'products'

	def get_queryset(self):
		farm=get_object_or_404(Farm,slug=self.kwargs['farm'])
		object_list=self.model.objects.filter(farm=farm,is_active=True).order_by('name')
		return object_list

	def get_context_data(self, **kwargs):
		farm=get_object_or_404(Farm,slug=self.kwargs['farm'])
		context = super(ProductsFarmView, self).get_context_data(**kwargs)
		context['farm']=get_object_or_404(FarmProfile,farm=farm)
		context['farmer_profile']=get_object_or_404(Profile,user=farm.user)
		context['feedback']=getFeedbackFarm(farm)
		context['farmer_name'] = getUserFullName(farm.user)
		context['categories']=Product.objects.filter(farm=farm,is_active=True).distinct('category')
		return context

class ShippingOptionList(LoggedInMixin,ListView):
	template_name = 'store/shipping_orders.html'
	context_object_name = 'shipping_options'
	paginate_by = 10

	def get_queryset(self):
		if haveFarm(self.request.user)==True:
			farm=getFarmUser(self.request.user)
			if farm.is_active:
				return ShippingOption.objects.filter(farm=farm).order_by('name')
			else:
				raise Http404("farm deactive")
		else:
			return redirect('register_farm')

class ShippingOptionDeleteView(LoggedInMixin,DeleteView):
	model = ShippingOption
	success_url = reverse_lazy('shipping_options')
	template_name = 'store/shipping_delete.html'

	def get_object(self,queryset=None):
		obj = super(ShippingOptionDeleteView, self).get_object()
		farm=getFarmUser(self.request.user)
		if farm.is_active:
			if not obj.farm == farm:
				raise Http404
			else:
				shippings = ShippingOption.objects.filter(farm=farm)
				if len(shippings) > 1:
					return obj
		else:
			raise Http404("farm deactive")


class ShippingOptionCreate(LoggedInMixin,CreateView):
	model = ShippingOption
	template_name = 'store/shipping_add.html'
	form_class = ShippingOptionForm
	success_url = reverse_lazy('shipping_options')

	def form_valid(self,form):
		self.object = form.save(commit=False)
		farm=getFarmUser(self.request.user)
		self.object.farm_id=farm.id
		shipping = form.cleaned_data['name']
		messages.success(self.request,"Has agreagado {0} a tu lista de envíos".format(shipping))
		return super(ShippingOptionCreate, self).form_valid(form)

class ShippingOptionUpdate(LoggedInMixin,UpdateView):
	model = ShippingOption
	template_name = 'store/shipping_update.html'
	form_class = ShippingOptionForm
	success_url = reverse_lazy('shipping_options')

	def get_object(self,queryset=None):
		obj = super(ShippingOptionUpdate, self).get_object()
		farm=getFarmUser(self.request.user)
		if farm.is_active:
			if not obj.farm == farm:
				raise Http404
			return obj
		else:
			raise Http404("farm deactive")

	def form_valid(self,form):
		shipping = form.cleaned_data['name']
		messages.success(self.request,"Has actualizado {0}".format(shipping))
		return super(ShippingOptionUpdate, self).form_valid(form)

class PaymentsList(LoggedInMixin,ListView):
	model = Payment
	template_name = 'store/payments.html'
	paginate_by = 10
	context_object_name= 'payments'

	def get_queryset(self):
		if haveFarm(self.request.user)==True:
			farm=getFarmUser(self.request.user)
			if farm.is_active:
				object_list=self.model.objects.filter(farm=farm)
				return object_list
			else:
				raise Http404("farm deactive")
		else:
			return redirect('register_farm')

class PaymentFarmDeleteView(LoggedInMixin,DeleteView):
	model = Payment
	success_url = reverse_lazy('payments')
	template_name = 'store/payment_delete.html'

	def get_object(self,queryset=None):
		obj = super(PaymentFarmDeleteView, self).get_object()
		farm=getFarmUser(self.request.user)
		if farm.is_active:
			if not obj.farm == farm:
				raise Http404
			else:
				payments = Payment.objects.filter(farm=farm)
				if len(payments) > 1:
					return obj
		else:
			raise Http404("farm deactive")

class PaymentFarmCreate(LoggedInMixin,CreateView):
	model = Payment
	template_name = 'store/payment_add.html'
	form_class = PayentForm
	success_url = reverse_lazy('payments')

	def form_valid(self,form):
		try:
			self.object = form.save(commit=False)
			farm=getFarmUser(self.request.user)
			self.object.farm_id=farm.id
			payment = form.cleaned_data['payment']
			form.save()
			messages.success(self.request,"Has agreagado {0} a tu lista de formas de pago".format(self.object.get_payment_display()))
			return HttpResponseRedirect(reverse_lazy('payments'))
		except IntegrityError:
			messages.error(self.request,"Esta forma de pago ya esta en tu lista".format(self.object.get_payment_display()))
			return HttpResponseRedirect(reverse_lazy('payment_add'))

class PaymentFarmUpdate(LoggedInMixin,UpdateView):
	model = Payment
	template_name = 'store/payment_update.html'
	form_class = PayentForm
	success_url = reverse_lazy('payments')

	def get_object(self,queryset=None):
		obj = super(PaymentFarmUpdate, self).get_object()
		farm=getFarmUser(self.request.user)
		if farm.is_active:
			if not obj.farm == farm:
				raise Http404
			return obj
		else:
			raise Http404("farm deactive")

	def form_valid(self,form):
		payment = form.cleaned_data['payment']
		messages.success(self.request,"Has actualizado {0}".format(self.object.get_payment_display()))
		return super(PaymentFarmUpdate, self).form_valid(form)

	def get_context_data(self, **kwargs):
		context = super(PaymentFarmUpdate, self).get_context_data(**kwargs)
		context['payment']=get_object_or_404(Payment,pk=self.kwargs['pk'])
		return context

class ProductFarmView(TemplateView):
	template_name='store/product_farm.html'

	def dispatch(self,request,*args,**kwargs):
		context=self.get_context_data()
		if request.method=='POST':
			ask_form = AskForm(request.POST)
			if ask_form.is_valid():
				ask=ask_form.cleaned_data['ask']
				buyer=request.user
				product=get_object_or_404(Product,slug=self.kwargs['product'])
				link=ask_form.save(commit=False)
				link.ask=ask
				link.buyer=buyer
				link.product=product
				link.seller=product.farm.user
				link.save()
				messages.success(request, 'Muy pronto resivirá respuesta por parte del vendedor!')
		return super(ProductFarmView,self).render_to_response(context)

	def get_context_data(self, **kwargs):
		ask_form = AskForm()
		product=get_object_or_404(Product,slug=self.kwargs['product'])
		if product.farm.is_active and product.is_active:
			context = super(ProductFarmView, self).get_context_data(**kwargs)
			context['product']=product
			context['fbProducts'] = getFeedbackProduct(product)
			context['feedback']=FeedbackProduct.objects.filter(order__product=product)
			context['shippings']=ShippingOption.objects.filter(farm=product.farm).order_by('name')
			context['farm']=get_object_or_404(FarmProfile,farm=product.farm)
			context['farmer_profile']=get_object_or_404(Profile,user=product.farm.user)
			context['ask_form']=ask_form
			context['categories']=Product.objects.filter(farm=product.farm,is_active=True).distinct('category')
			context['comments']=ProductComments.objects.all().filter(product=product).order_by('-date_post_ask')
			context['latest_products']=Product.objects.filter(farm=product.farm, is_active=True).order_by('?')[:15]
			context['farmer_name'] = getUserFullName(product.farm.user)
			return context
		else:
			raise Http404

class FarmsView(ListView):
	model = FarmProfile
	template_name='store/farms.html'
	paginate_by=20
	context_object_name= 'farms'

	def get_queryset(self):
		object_list=self.model.objects.filter(farm__is_active=True).order_by('farm')
		return object_list

class FarmCategoryProductsView(ListView):
	model = Product
	template_name='store/category_product_farm.html'
	paginate_by=20
	context_object_name= 'products'

	def get_queryset(self):
		farm=get_object_or_404(Farm,slug=self.kwargs['farm'])
		if farm.is_active:
			category=get_object_or_404(ProductCategory,slug=self.kwargs['category'])
			object_list=self.model.objects.filter(category=category,farm=farm,is_active=True)
			return object_list
		else:
			raise Http404

	def get_context_data(self, **kwargs):
		category=get_object_or_404(ProductCategory,slug=self.kwargs['category'])
		context = super(FarmCategoryProductsView, self).get_context_data(**kwargs)
		farm=get_object_or_404(Farm,slug=self.kwargs['farm'])
		context['farm']=get_object_or_404(FarmProfile,farm=farm)
		context['category']=category
		context['feedback']=getFeedbackFarm(farm)
		context['categories']=Product.objects.filter(farm=farm,is_active=True).distinct('category')
		context['farmer_name'] = getUserFullName(farm.user)
		context['farmer_profile']=get_object_or_404(Profile,user=farm.user)
		return context

class FarmFeedbackView(ListView):
	model = FeedbackSeller
	template_name='store/feedback_farm.html'
	paginate_by=20
	context_object_name= 'feedback_farm'

	def get_queryset(self):
		farm=get_object_or_404(Farm,slug=self.kwargs['farm'])
		if farm.is_active:
			object_list=self.model.objects.filter(order__farm=farm)
			return object_list
		else:
			raise Http404

	def get_context_data(self, **kwargs):
		context = super(FarmFeedbackView, self).get_context_data(**kwargs)
		farm=get_object_or_404(Farm,slug=self.kwargs['farm'])
		context['farm']=get_object_or_404(FarmProfile,farm=farm)
		context['feedback']=getFeedbackFarm(farm)
		context['categories']=Product.objects.filter(farm=farm,is_active=True).distinct('category')
		context['farmer_name'] = getUserFullName(farm.user)
		context['farmer_profile']=get_object_or_404(Profile,user=farm.user)
		return context

class UserFeedbackView(LoggedInMixin,ListView):
	model = FeedbackSeller
	template_name='farm/feedback.html'
	paginate_by=20
	context_object_name= 'feedback_farm'

	def get_queryset(self):
		if haveFarm(self.request.user)==True:
			farm=getFarmUser(self.request.user)
			if farm.is_active:
				object_list = self.model.objects.filter(order__farm=farm)
				for obj in object_list:
					if not obj.reply:
						setattr(obj,'reply_form',ReplyFeedbackForm())
					setattr(obj,'full_name',User.objects.getFullName(obj.order.buyer))
				return object_list
			else:
				raise Http404("farm deactive")
		else:
			return redirect('register_farm')

	def get_context_data(self, **kwargs):
		context = super(UserFeedbackView, self).get_context_data(**kwargs)
		farm=getFarmUser(self.request.user)
		context['farm']=get_object_or_404(FarmProfile,farm=farm)
		context['feedback']=getFeedbackFarm(farm)
		context['categories']=Product.objects.filter(farm=farm,is_active=True).distinct('category')
		context['farmer_name'] = getUserFullName(farm.user)
		context['farmer_profile']=get_object_or_404(Profile,user=farm.user)
		return context

	def post(self,request,*args,**kwargs):
		for key in request.POST:
			if key.startswith('btnReply'):
					feedback_id = key[8:]
					reply=request.POST['reply']
					feedback=get_object_or_404(FeedbackSeller,id=feedback_id)
					feedback.reply=reply
					feedback.save()
					PurchaseRecord(purchase_order_id=feedback.order.id,state=4,detail='Ha comentado tu calificación').save()
					notificationOrderSeller(request.user,feedback.order.buyer,feedback.order)
					messages.success(self.request, 'Publicación exitosa!')
		return HttpResponseRedirect(reverse('feedback'))

class FarmCategoryView(ListView):
	model = Product
	template_name='store/category_farm.html'
	paginate_by=20
	context_object_name= 'products'

	def get_queryset(self):
		farm=get_object_or_404(Farm,slug=self.kwargs['farm'])
		if farm.is_active:
			object_list=self.model.objects.filter(farm=farm,is_active=True)
			return object_list
		else:
			raise Http404

	def get_context_data(self, **kwargs):
		context = super(FarmCategoryView, self).get_context_data(**kwargs)
		farm=get_object_or_404(Farm,slug=self.kwargs['farm'])
		categories=Product.objects.values('category','farm').annotate(count=Count('category')).order_by('category').filter(farm=farm,is_active=True)
		for category in categories:
			category['category']=get_object_or_404(ProductCategory,pk=category['category'])
		context['feedback']=getFeedbackFarm(farm)
		context['categories']=categories
		context['farm']=get_object_or_404(FarmProfile,farm=farm)
		context['farmer_name'] = getUserFullName(farm.user)
		context['farmer_profile']=get_object_or_404(Profile,user=farm.user)
		return context

class ShoppingCarView(TemplateView):
	template_name = 'store/shopping_cart.html'

class UsersView(ListView):
	model = Profile
	template_name='store/users.html'
	paginate_by=20
	context_object_name= 'users'

	def get_queryset(self):
		object_list=self.model.objects.all().order_by('user')
		for obj in object_list:
			obj.user_name = getUserFullName(obj.user)
		return object_list

class GeoFarmView(TemplateView):
    template_name = 'store/geo-farm.html'

    def get_context_data(self, **kwargs):
		context = super(GeoFarmView, self).get_context_data(**kwargs)
		context['categories']=ProductCategory.objects.all().order_by('name')
		categories=Product.objects.filter(farm__is_active=True,is_active=True).values('category').annotate(count=Count('farm', distinct='farm')).order_by('category')
		for category in categories:
			category['category']=ProductCategory.objects.get(pk=category['category'])
		context['total_farms']=len(Farm.objects.filter(is_active=True))
		context['categories']=categories
		return context

class ShopSuccessView(LoggedInMixin,TemplateView):
	template_name = 'store/shop_success.html'

class ShippingAddressView(LoggedInMixin,TemplateView):
	template_name = 'store/shipping_address.html'

	def post(self,request,*args,**kwargs):
		shippingForm = ShippingAddressForm(request.POST)
		if shippingForm.is_valid():
			try:
				address=ShippingAddress.objects.get(user=request.user)
				address.neighborhood=shippingForm.cleaned_data['neighborhood']
				address.address=shippingForm.cleaned_data['address']
				address.city=shippingForm.cleaned_data['city']
				address.phone=shippingForm.cleaned_data['phone']
				address.description=shippingForm.cleaned_data['description']
				address.save()
				if 'shopping_cart' in request.POST:
					data = json.loads(request.POST['shopping_cart'])
					shopping_cart = data['product']
					for product_cart in shopping_cart:
						product = Product.objects.get(slug=product_cart['product_slug'])
						shipping_option = ShippingOption.objects.get(id=product_cart['shipping_id'])
						quantity = product_cart['quantity']
						payment =product_cart['payment_id']
						PurchaseOrder.objects.create_order(product=product,shipping_option=shipping_option,quantity=quantity,payment_id=payment,user=request.user,address=address)
					return HttpResponseRedirect(reverse('shop_success'))
				else:
					messages.error(self.request, 'Por favor compra algunos productos')
			except Exception as e:
				print e
				messages.error(self.request, 'Por favor diligencie el formulario!')
			except ShippingAddress.DoesNotExist:
				link = shippingForm.save(commit=False)
				link.user=request.user
				link.save()
				return HttpResponseRedirect(reverse('shop_success'))
		else:
			messages.error(self.request, 'Por favor diligencie el formulario!')
		return HttpResponseRedirect(reverse('shipping'))

	def get_context_data(self,**kwargs):
		context= super(ShippingAddressView, self).get_context_data(**kwargs)
		try:
			address=ShippingAddress.objects.get(user=self.request.user)
			context['shipping_form'] =ShippingAddressForm(instance=address)
		except ShippingAddress.DoesNotExist:
			context['shipping_form'] = ShippingAddressForm()
		return context

class AddressView(LoggedInMixin,TemplateView):
	template_name = 'farm/shipping_address.html'

	def post(self,request,*args,**kwargs):
		shippingForm = ShippingAddressForm(request.POST or None)
		template_name = 'farm/shipping_address.html'
		if shippingForm.is_valid():
			try:
				shipping=ShippingAddress.objects.get(user=request.user)
				shipping.neighborhood=shippingForm.cleaned_data['neighborhood']
				shipping.address=shippingForm.cleaned_data['address']
				shipping.city=shippingForm.cleaned_data['city']
				shipping.phone=shippingForm.cleaned_data['phone']
				shipping.description=shippingForm.cleaned_data['description']
				shipping.save()
				messages.success(self.request, 'Información actualizada!')
				return HttpResponseRedirect(reverse('address'))
			except ShippingAddress.DoesNotExist:
				link = shippingForm.save(commit=False)
				link.user=request.user
				link.save()
				messages.success(self.request, 'Información actualizada!')
				return HttpResponseRedirect(reverse('address'))
		else:
			messages.error(self.request, 'Por favor diligencie el formulario!')
		return render(self.request, template_name, {'shipping_form':shippingForm})

	def get_context_data(self,**kwargs):
		context= super(AddressView, self).get_context_data(**kwargs)
		try:
			address=ShippingAddress.objects.get(user=self.request.user)
			context['shipping_form'] =ShippingAddressForm(self.request.POST or None, instance=address)
		except ShippingAddress.DoesNotExist:
			context['shipping_form'] = ShippingAddressForm(self.request.POST or None)
		return context

class PurchaseOrderList(LoggedInMixin,ListView):
	model = PurchaseOrder
	template_name = 'store/purchase_orders.html'
	paginate_by = 20
	context_object_name = 'orders'

	def get_queryset(self):
		object_list = self.model.objects.filter(farm__user=self.request.user).order_by('-date')
		return object_list

class OrderSellerView(LoggedInMixin,TemplateView):
	template_name = 'store/order_seller.html'

	def get_context_data(self,**kwargs):
		context = super(OrderSellerView,self).get_context_data(**kwargs)
		order = get_object_or_404(PurchaseOrder,id=kwargs['pk'])
		if order.farm.user==self.request.user:
			if 'state' in self.request.GET:
				notifications=Notification.objects.get(id=self.request.GET['state'])
				notifications.mark_as_read()
			try:
				fbProducts=FeedbackProduct.objects.get(order=order)
				context['fbProducts']=fbProducts
				if fbProducts:
					fbSeller=FeedbackSeller.objects.get(order=order)
					if not fbSeller.reply:
						setattr(fbSeller,'reply_form',ReplyFeedbackForm())
					context['fbSeller']=fbSeller
			except FeedbackProduct.DoesNotExist as e:
				context['fbProducts']=None


			context['order_form'] = PurchaseOrderForm(instance=order)
			context['order']=order
		else:
			raise Http404
		return context

	def post(self,request,*args,**kwargs):
		order_id=kwargs['pk']
		if 'reply' in request.POST:
			reply=request.POST['reply']
			feedback=get_object_or_404(FeedbackSeller,order_id=order_id)
			feedback.reply=reply
			feedback.save()
			PurchaseRecord(purchase_order_id=feedback.order.id,state=4,detail='Ha comentado tu calificación').save()
			notificationOrderSeller(request.user,feedback.order.buyer,feedback.order)
			messages.success(self.request, 'Publicación exitosa!')
		if 'state' in request.POST:
			state = request.POST['state']
			order = get_object_or_404(PurchaseOrder,id=order_id)
			old_state = order.get_state_display()
			order.state = request.POST['state']
			order.save()
			order = get_object_or_404(PurchaseOrder,id=order_id)
			new_state = order.get_state_display()
			PurchaseRecord(purchase_order_id=order_id,state=2,detail='La orden ha pasado de %s a %s'%(old_state,new_state)).save()
			notificationOrderSeller(request.user,order.buyer,order)
			messages.success(request, 'Has cambiado el estado de esta orden!')
		if 'message' in request.POST:
			order = get_object_or_404(PurchaseOrder,id=order_id)
			PurchaseRecord(purchase_order_id=order_id,state=4,detail=request.POST['message']).save()
			notificationOrderSeller(request.user,order.buyer,order)
			messages.success(request, 'Mensaje enviado!')
		return HttpResponseRedirect(reverse('order_seller',kwargs={'pk':order_id}))

class MyShoppingList(LoggedInMixin,ListView):
	model = PurchaseOrder
	template_name = 'store/my_shopping.html'
	paginate_by = 20
	context_object_name = 'orders'

	def get_queryset(self):
		object_list = self.model.objects.filter(buyer=self.request.user).order_by('-date')
		return object_list

class OrderBuyerView(LoggedInMixin,TemplateView):
	template_name = 'store/order_buyer.html'

	def get_context_data(self,**kwargs):
		context = super(OrderBuyerView,self).get_context_data(**kwargs)
		order = get_object_or_404(PurchaseOrder,id=kwargs['pk'])
		if order.buyer==self.request.user:
			if 'state' in self.request.GET:
				notifications=Notification.objects.get(id=self.request.GET['state'])
				notifications.mark_as_read()
			context['order']=order
		else:
			raise Http404
		return context

	def post(self,request,*args,**kwargs):
		order_id=kwargs['pk']
		if 'message' in request.POST:
			order = get_object_or_404(PurchaseOrder,id=order_id)
			PurchaseRecord(purchase_order_id=order_id,state=3,detail=request.POST['message']).save()
			notificationOrderBuyer(request.user,order.farm.user,order)
			messages.success(request, 'Mensaje enviado!')
		return HttpResponseRedirect(reverse('order_buyer',kwargs={'pk':order_id}))

class FeedbackOrderView(LoggedInMixin,TemplateView):
	template_name = 'store/feedback_order.html'

	def get_context_data(self,**kwargs):
		context = super(FeedbackOrderView, self).get_context_data(**kwargs)
		order = get_object_or_404(PurchaseOrder,id=kwargs['pk'])
		if order.received:
			raise Http404
		elif order.buyer==self.request.user:
			context['fb_seller']=FeedbackSellerForm(self.request.POST or None)
			context['fb_product']=FeedbackProductForm(self.request.POST or None)
			context['order']=order
		else:
			raise Http404
		return context

	def post(self,request,*args,**kwargs):
		order=PurchaseOrder.objects.get(id=kwargs['pk'])
		try:
			comment= request.POST['comment']
			price= request.POST['price']
			quality= request.POST['quality']
			description= request.POST['description']
			FeedbackProduct(order_id=order.id,comment=comment,price=price,quality=quality,description=description).save()

			observations = request.POST['observations']
			communication=request.POST['communication']
			responsibility=request.POST['responsibility']
			quickness=request.POST['quickness']
			FeedbackSeller(order_id=order.id,observations=observations,communication=communication,quickness=quickness,responsibility=responsibility).save()

			order.received=True
			order.state=3
			order.save()
			notificationOrderBuyer(request.user,order.farm.user,order)
			PurchaseRecord(purchase_order_id=order.id,state=2,detail='Ha recibido la orden').save()
			messages.success(request, 'Has calificado tu orden!')
			return HttpResponseRedirect(reverse('order_buyer',kwargs={'pk':order.id}))

		except Exception as e:
			messages.error(request, 'Tenemos un problema!')
			return HttpResponseRedirect(reverse('order_buyer',kwargs={'pk':order.id}))

class StatisticsView(LoggedInMixin,TemplateView):
	template_name = "store/statistics.html"

	def get_context_data(self):
		context = super(StatisticsView,self).get_context_data()
		farm=getFarmUser(self.request.user)
		context['total_sales']=PurchaseOrder.objects.total(farm)
		context['farm']=get_object_or_404(FarmProfile,farm=farm)
		context['day_sales']=PurchaseOrder.objects.day_sales(farm=farm)
		context['week_sales']=PurchaseOrder.objects.week_sales(farm=farm)
		context['month_sales']=PurchaseOrder.objects.month_sales(farm=farm)
		context['year_sales']=PurchaseOrder.objects.year_sales(farm=farm)
		context['origin_sales']=PurchaseOrder.objects.origin_sales(farm=farm)
		context['categories']=Product.objects.filter(farm=farm,is_active=True).distinct('category')
		context['farmer_name'] = getUserFullName(farm.user)
		context['farmer_profile']=get_object_or_404(Profile,user=farm.user)
		return context

class MailboxList(LoggedInMixin,ListView):
    model = Mailbox
    template_name = 'store/mailbox.html'
    paginate_by = 10
    context_object_name = 'suggestings'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Mailbox.objects.all().order_by('-date')
        else:
            raise Http404

class MailboxView(LoggedInMixin,DetailView):
    model = Mailbox
    context_object_name ='suggesting'

    def get_object(self,queryset=None):
	if self.request.user.is_superuser:
            obj = super(MailboxView, self).get_object()
	    return obj
        else:
            raise Http404

    def post(self,request,*args,**kwargs):
    	obj = super(MailboxView, self).get_object()
    	obj.reply = request.POST['reply']
    	obj.save()
    	messages.success(request, 'Has dado respuesta a esta sugerencia!')
    	return HttpResponseRedirect(reverse('mailbox_response',kwargs={'pk':obj.id}))

def shoppingCart(request):
	data=True
	if request.is_ajax:
		if request.method=='POST':
			ShoppingCart.objects.filter(user=request.user).delete()
		 	objects = json.loads(request.POST['shopping_cart'])
			for obj in objects:
				iObj = json.loads(obj)
				product = Product.objects.get(slug=iObj['product_slug'])
				quantity = iObj['n_quantity']
				shipping =iObj['shipping_id']
				try:
					cart = ShoppingCart.objects.get(user=request.user,product=product)
					cart.quantity = quantity
					cart.shipping_id =shipping
					cart.save()
				except Exception:
					cart = ShoppingCart(user=request.user,product=product,quantity=quantity,shipping_id=shipping)
					cart.save()
	else:
		data=False
	return HttpResponse(data, content_type="text/plain")

def addProductCart(request):
	data=True
	if request.is_ajax:
		if request.method=='POST':
		 	shop = json.loads(request.POST['shopping_cart'])
			product = Product.objects.get(slug=shop['product_slug'])
			quantity = shop['n_quantity']
			shipping =shop['shipping_id']
			try:
				cart = ShoppingCart.objects.get(user=request.user,product=product)
				cart.quantity = quantity
				cart.shipping_id =shipping
				cart.save()
			except Exception:
				cart = ShoppingCart(user=request.user,product=product,quantity=quantity,shipping_id=shipping)
				cart.save()
	else:
		data=False
	return HttpResponse(data, content_type="text/plain")

def delProductCart(request):
	data=True
	if request.is_ajax:
		if request.method=='POST':
			slug = request.POST['shopping_cart']
			ShoppingCart.objects.get(user=request.user,product__slug=slug).delete()
	else:
		data=False
	return HttpResponse(data, content_type="text/plain")

def sendMailbox(request):
	data= True
	if request.is_ajax:
		if request.method=='POST':
			phone=request.POST['phone']
			user=request.POST['user']
			email=request.POST['email']
			message=request.POST['message']
			Mailbox(phone=phone,user=user,email=email,message=message).save()
	else:
		data=False
	return HttpResponse(data, content_type="text/plain")

def getShoppingCart(user):
	cart=ShoppingCart.objects.filter(user=user)
	shop = []
	for c in cart:
		item = {}
		item['product_slug']=c.product.slug
		item['farm_slug']=c.product.farm.slug
		item['image']=c.product.image.url
		item['price']=c.product.price
		item['farm']=c.product.farm.name
		item['product_name']=c.product.name
		item['n_quantity']=c.quantity
		item['shipping_price']=c.shipping.price
		item['shipping']=c.shipping.name
		item['shipping_id']=c.shipping.id
		shop.append(item)
	return shop
