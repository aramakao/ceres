#-*- encoding: utf-8 -*-
from __future__ import unicode_literals
from apps.account.models import User,StateUserComment, Profile, Friend, StateUser, is_session, InivitationFriend, remove_session
from apps.product.models import Product, ProductCategory
from django.contrib.auth.views import password_reset
from apps.blog.models import Blog
from apps.farm.models import Farm
from apps.store.models import Mailbox, FeedbackProduct, ProductComments, ShippingOption, Payment, ShippingAddress
from apps.groups.models import *
from apps.extras.models import City
from apps.message.models import Message
from apps.blog.models import Blog
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import *
from django.shortcuts import get_object_or_404
from django.db.models import Count
from datetime import datetime
from django.utils.timesince import timesince
from decimal import *
from django.contrib.auth import authenticate,login
import json
from django.db import IntegrityError
from apps.ceres.notification import *
import youtube_dl

class UserViewSet(viewsets.ModelViewSet):
	queryset=Profile.objects.all().order_by('username','first_name','last_name')
	serializer_class = UserMinSerializer

class UserProfileMinViewSet(viewsets.ViewSet):
	def list(self,request):
		profiles=Profile.objects.all().order_by('user')
		serializer= UserProfileMinSerializer(profiles,many=True,context={'request':request})
		return Response(serializer.data)

	def retrieve(self,request,slug=None):
		profile = Profile.objects.get(user__username=slug)
		serializer = UserProfileSerializer(profile,many=False,context={'request':request})
		return Response(serializer.data)

	def min(self,request,slug=None):
		profile = Profile.objects.get(user__username=slug)
		serializer = UserProfileMinSerializer(profile,many=False,context={'request':request})
		return Response(serializer.data)

	def shippingAddress(self,request,slug=None,token=None):
		try:
			if is_session(session_key=token):
				address = ShippingAddress.objects.get(user__username=slug)
				serializer = ShippingAddressSerializer(address,context={'request':request})
				return Response(serializer.data)
			else:
				return Response({'session':False})
		except Exception as e:
			print e
			return Response({'server':False})

class FriendsViewSet(viewsets.ViewSet):
	def list(self,request,slug=None):
		friends=Friend.objects.filter(user__username=slug)
		serializer = FriendSerializer(friends,many=True,context={'request':request})
		return Response(serializer.data)

class GroupsUserViewSet(viewsets.ViewSet):
	def list(self,request,slug=None):
		groups=GroupMember.objects.filter(user__username=slug)
		serializer = GroupsUserSerializer(groups,many=True,context={'request':request})
		return Response(serializer.data)

class BannerViewSet(viewsets.ModelViewSet):
	def list(self,request):
		banners = Blog.objects.filter(in_banner=True)
		serializer=BannerSerializer(banners,many=True,context={'request': request})
		return Response(serializer.data)

class ProductViewSet(viewsets.ViewSet):

	def list(self,request):
		products = Product.objects.all()
		serializer=ProductSerializer(products,many=True,context={'request': request})
		return Response(serializer.data)

	def retrieve(self,request,slug=None):
		product = get_object_or_404(Product,slug=slug)
		product.profile= FarmProfile.objects.get(farm=product.farm)
		serializer=ProductSerializer(product,context={'request': request})
		return Response(serializer.data)

class ProductCommentsViewSet(viewsets.ModelViewSet):
	def retrieve(self,request,product=None):
		comments = ProductComments.objects.filter(product__slug=product).order_by('-date_post_ask')
		serializer = ProductCommentsSerializer(comments,many=True,context={'request':request})
		return Response(serializer.data)

	def feedback(self,request,product=None):
		try:
			feedback = FeedbackProduct.objects.filter(order__product__slug=product)
			print feedback
			serializer = FeedbackProductSerializer(feedback,many=True,context={'request':request})
			return Response(serializer.data)
		except Exception as e:
			print e
			raise

class AgroBlogViewSet(viewsets.ViewSet):
	def list(self,request):
		entries = Blog.objects.all().order_by('posted')
		serializer = EntryMinSerializar(entries,many=True,context={'request':request})
		return Response(serializer.data)

	def retrieve(self,request,slug=None):
		entry = get_object_or_404(Blog,slug=slug)
		serializer = EntrySerializar(entry,context={'request':request})
		return Response(serializer.data)

class CategoryListViewSet(viewsets.ViewSet):
	def list(self,request):
		categories = ProductCategory.objects.all().order_by('name')
		serializer = CategoryProductSerializer(categories, many=True, context={'request':request})
		return Response(serializer.data)

	def retrieve(self,request,pk=None):
		category=get_object_or_404(ProductCategory,slug=pk)
		serializer=CategoryProductSerializer(category,context={'request':request})
		return Response(serializer.data)

class CategoryEntriesViewSet(viewsets.ViewSet):
	def list(self,request,slug=None):
		categories = Blog.objects.filter(category__slug=slug).order_by('posted')
		serializer = EntryMinSerializar(categories, many=True, context={'request':request})
		return Response(serializer.data)

class LatestProductViewSet(viewsets.ViewSet):

	def list(self,request):
		products = Product.objects.filter(is_active=True)[:15]
		serializer=LatestProductSerializer(products, many=True, context={'request': request})
		return Response(serializer.data)

class AllProductMinViewSet(viewsets.ViewSet):
	def list(self,request):
		products = Product.objects.filter(is_active=True).order_by('name')
		serializer=ProductMinSerializer(products, many=True, context={'request': request})
		return Response(serializer.data)

class AllGroupMinViewSet(viewsets.ViewSet):
	def list(self,request):
		groups = Group.objects.filter(is_active=True).order_by('name')
		serializer=GroupSerializer(groups, many=True, context={'request': request})
		return Response(serializer.data)

	def retrieve(self,request,slug=None):
		profile=get_object_or_404(GroupProfile,group__slug=slug)
		serializer=GroupProfileSerializer(profile,context={'request':request})
		return Response(serializer.data)

class GroupMembersViewSet(viewsets.ViewSet):
	def list(self,request,slug=None):
		members = GroupMember.objects.filter(group__slug=slug)
		serializer=GroupMemberSerializer(members, many=True, context={'request': request})
		return Response(serializer.data)

class GroupProductsViewSet(viewsets.ViewSet):
	def list(self,request,slug=None):
		group = Group.objects.get(slug=slug)
		products = group.getProducts()
		serializer=ProductMinSerializer(products, many=True, context={'request': request})
		return Response(serializer.data)

class ProductsCategory(viewsets.ViewSet):
	def list(self,request,pk=None):
		products = Product.objects.filter(is_active=True, category__slug=pk).order_by('name')
		serializer=ProductMinSerializer(products, many=True, context={'request': request})
		return Response(serializer.data)

class GeoFarmCountCityViewSet(viewsets.ViewSet):

	def list(self,request):
		farms=FarmProfile.objects.filter(farm__is_active=True).values('location','location_slug').annotate(count=Count('location'))
		serializer=GeoFarmsCountCitySerializer(farms,many=True)
		return Response(serializer.data)

class GeoFarmCategory(viewsets.ModelViewSet):

	def list(self,request,slug=None):
		category = ProductCategory.objects.get(slug=slug)
		farms = Product.objects.values('farm').filter(category=category,farm__is_active=True,is_active=True).distinct('farm')
		profiles = []
		for farm in farms:
			profile=FarmProfile.objects.get(farm=farm['farm'])
			profiles.append(profile)
		serializer=FarmProfileSerializer(profiles,many=True)
		return Response(serializer.data)

	def all(self,request,slug=None):
		farms = FarmProfile.objects.filter(farm__is_active=True)
		serializer=FarmProfileSerializer(farms,many=True)
		return Response(serializer.data)

class FarmsProfileViewSet(viewsets.ModelViewSet):

	def list(self,request,slug=None):
		farms=FarmProfile.objects.filter(location_slug=slug)
		serializer=FarmProfileSerializer(farms,many=True)
		return Response(serializer.data)

class FarmsViewSet(viewsets.ModelViewSet):
	def list(self,request):
		farms = Farm.objects.all()
		serializer = FarmSerializer(farms,many=True,context={'request': request})
		return Response(serializer.data)

	def retrieve(self,request,slug=None):
		farmProfile = get_object_or_404(FarmProfile,farm__slug=slug)
		userProfile= get_object_or_404(Profile,user=farmProfile.farm.user)
		products = farmProfile.farm.get_last_products()
		setattr(farmProfile,'profile',userProfile)
		setattr(farmProfile,'products',products)
		serializer = FarmProfileSerializer(farmProfile,context={'request':request})
		return Response(serializer.data)

class BuyOptionsViewSet(viewsets.ModelViewSet):
	def list(self,request,slug=None):
		shippings = ShippingOption.objects.filter(farm__slug=slug)
		payments = Payment.objects.filter(farm__slug=slug)
		payment_serializer = PaymentOptionSerializer(payments,many=True,context={'request':request})
		shipping_serializer = ShippingOptionSerializer(shippings,many=True,context={'request':request})
		return Response({'payments':payment_serializer.data,'shipping':shipping_serializer.data})

class PaymentsOptionsViewSet(viewsets.ModelViewSet):
	def list(self,request,slug=None):
		payments = Payment.objects.filter(farm__slug=slug)
		payment_serializer = PaymentOptionSerializer(payments,many=True,context={'request':request})
		return Response(payment_serializer.data)

class ProductsFarmViewSet(viewsets.ModelViewSet):
	def list(self,request,slug=None):
		products = Product.objects.filter(farm__slug=slug,is_active=True)
		serializer = ProductWithoutFarmSerializer(products,many=True,context={'request':request})
		return Response(serializer.data)

class StatesUserViewSet(viewsets.ViewSet):
	def min(self,request,slug=None):
		states = StateUser.objects.filter(user__username=slug).order_by('-date')[:10]
		serializer = StateUserSerializer(states,many=True,context={'request':request})
		return Response(serializer.data)

	def list(self,request,slug=None):
		states = StateUser.objects.filter(user__username=slug).order_by('-date')
		serializer = StateUserSerializer(states,many=True,context={'request':request})
		return Response(serializer.data)

	def comments(self, request,slug=None, pk=None):
		comments=StateUserComment.objects.filter(state=pk).order_by('-date')
		serializer = StateCommentsSerializer(comments,many=True,context={'request':request})
		return Response(serializer.data)

class StatusCommentsViewSet(viewsets.ViewSet):
	def list(self,request,pk=None):
		comments=StateUserComment.objects.filter(state=pk).order_by('-date')
		_comments =[]
		for comment in comments:
			comment.date_post=timesince(comment.date)
			_comments.append(comment)
		serializer=StatusCommentsSerializer(_comments,many=True,context={'request': request})
		for data in serializer.data:
			user = User.objects.get(username=data['user']['username'])
			data['user']['full_name']=getUserFullName(user)
		return Response(serializer.data)

class StatusGroupCommentsViewSet(viewsets.ViewSet):

	def list(self,request,pk=None):
		comments=StateGroupComment.objects.filter(state=pk)
		_comments =[]
		for comment in comments:
			comment.date_post=timesince(comment.date)
			_comments.append(comment)
		serializer=StatusGroupCommentsSerializer(_comments,many=True,context={'request': request})
		for data in serializer.data:
			user = User.objects.get(username=data['user']['username'])
			data['user']['full_name']=getUserFullName(user)
		return Response(serializer.data)

class SearchViewSet(viewsets.ViewSet):
	def list(Self,request,word=None):
		results = Index.objects.min_search(word.lower())
		serializer=IndexMinSerializer(results,many=True)
		return Response(serializer.data)

class QuestionViewSet(viewsets.ModelViewSet):
	def list(self,request):
		questions = Question.objects.filter(is_active=True)
		serializer = QuestionSerilizer(questions,many=True,context={'request':request})
		return Response(serializer.data)

class MainViewSet(viewsets.ViewSet):
	def list(self,request):
		banners = Blog.objects.filter(in_banner=True)
		products = Product.objects.filter(farm__is_active=True,is_active=True).order_by('-id')[:15]
		entries = Blog.objects.all().order_by('posted')[:10]
		users = User.objects.all().order_by('?')[:5]
		farms = Farm.objects.all().order_by('?')[:10]
		status = StateUser.objects.all().order_by('-date')[:10]
		groups = Group.objects.all().order_by('?')[:10]
		serializer_banner = BannerSerializer(banners,many=True,context={'request':request})
		serializer_products = ProductMinSerializer(products,many=True,context={'request':request})
		serializer_entries = EntryMinSerializar(entries,many=True,context={'request':request})
		serializer_users = UserMinSerializer(users,many=True,context={'request':request})
		serializer_farms = FarmSerializer(farms,many=True,context={'request':request})
		serializer_status = StateSerializer(status,many=True,context={'request':request})
		serializer_groups = GroupSerializer(groups,many=True,context={'request':request})
		serializer = []
		serializer.append({'banners':serializer_banner.data})
		serializer.append({'latest_products':serializer_products.data})
		serializer.append({'entries':serializer_entries.data})
		serializer.append({'users':serializer_users.data})
		serializer.append({'farms':serializer_farms.data})
		serializer.append({'status':serializer_status.data})
		serializer.append({'groups':serializer_groups.data})
		return Response(serializer)

class StatusViewSet(viewsets.ViewSet):
	def list(self,request):
		status = StateUser.objects.all().order_by('-date')
		serializer = StateSerializer(status,many=True,context={'request':request})
		return Response(serializer.data)

class GeoFarmViewSet(viewsets.ViewSet):
	def all(self,request):
		geos = FarmProfile.objects.values('latitude','longitude','farm__name','slogan','farm__slug').filter(farm__is_active=True)
		serializer_geo = GeoFarmSerializar(geos,many=True,context={'request': request})
		categories = Product.objects.counCategories()
		#serializer_categories = CategoryCountSerializer(categories,many=True)
		serializer = []
		serializer.append({'geo':serializer_geo.data})
		serializer.append({'category':categories})
		return Response(serializer)

	def category(self,request,slug=None):
		#geos = FarmProfile.objects.values('latitude','longitude','farm__name','slogan','farm__slug').filter(farm__is_active=True)
		category = ProductCategory.objects.get(slug=slug)
		farms = Product.objects.values('farm').filter(category=category,farm__is_active=True,is_active=True).distinct('farm')

		profiles = []
		for farm in farms:
			profile=FarmProfile.objects.values('latitude','longitude','farm__name','slogan','farm__slug').get(farm=farm['farm'])
			profiles.append(profile)
		serializer_geo = GeoFarmSerializar(profiles,many=True,context={'request': request})
		serializer_category = CategoryMinSerializer(category,many=False,context={'request': request})
		serializer = []
		serializer.append({'geo':serializer_geo.data})
		serializer.append({'category':serializer_category.data})

		return Response(serializer)

class LoginViewSet(viewsets.ViewSet):
	def post(self,request,user=None):
		try:
			user = authenticate(username=request.DATA['user'], password=request.DATA['password'])
			if user is not None:
				login(request, user)
				profile = Profile.objects.get(user=user)
				serializer_profile = UserProfileMinSerializer(profile,many=False,context={'request':request})
				request.session.set_expiry(600)
				return Response({"login":True,"session":request.session.session_key,"profile":serializer_profile.data})
			else:
				data = False
				return Response({"login":False,"session":False})
		except Exception as e:
			return Response({"login":False,"session":False})

	def is_auth(self,request,user=None):
		is_session(session_key=user)
		return Response(is_session(session_key=user))

class RegisterViewSet(viewsets.ViewSet):
	def post(self,request,user=None):
		try:
			username = request.DATA['username']
			email = request.DATA['email']
			password = request.DATA['password']
			User.objects.create_user(username,email,password)
			user= authenticate(username=username,password=password)
			login(request,user)
			profile = Profile.objects.get(user=user)
			serializer_profile = UserProfileMinSerializer(profile,many=False,context={'request':request})
			request.session.set_expiry(600)
			return Response({"register":True,"session":request.session.session_key,"profile":serializer_profile.data})
		except Exception as e:
			return Response({"register":False})

class LogoutViewSet(viewsets.ViewSet):
	def post(self,request,key=None):
		try:
			key = request.DATA['session_key']
			result = remove_session(session_key=key)
			return Response({"logout":result})
		except Exception as e:
			return Response({"logout":False})

class MailboxViewSet(viewsets.ViewSet):
	def post(self,request,format=None):
		try:
			serializer = MailboxSerializer(data=request.DATA)
			if serializer.is_valid():
				serializer.save()
				return Response({"mailbox":True})
			else:
				return Response({"mailbox":False})
		except Exception as e:
			return Response({"mailbox":False})

class FinishShopViewSet(viewsets.ViewSet):
	def post(self,request,token=None):
		try:
			if is_session(request.DATA['token']):
				user =User.objects.get(username=request.DATA['user'])
				shipping_json = json.loads(request.DATA['shipping'])
				shipping = ShippingAddress.objects.get(user=user)
				shipping.address=shipping_json['address']
				shipping.neighborhood=shipping_json['neighborhood']
				shipping.city=shipping_json['city']
				shipping.phone=shipping_json['phone']
				shipping.description=shipping_json['description']
				shipping.save()
				products_json = json.loads(request.DATA['products'])

				for product in products_json:
					prod = Product.objects.get(slug=product['productSlug'])
					payment = id=int(product['paymentId'])
					shipping_option = ShippingOption.objects.get(id=product['shippingId'])
					quantity = product['quantity']
					PurchaseOrder.objects.create_order(product=prod,shipping_option=shipping_option,quantity=quantity,payment_id=payment,user=user,address=shipping)
				return Response({"shop_end":True})
			else:
				return Response({"session_key":False})
		except Exception as e:
			return Response({"session_key":False})


class MessageViewSet(viewsets.ViewSet):
	def post(self,request,token=None):
		try:
			if is_session(request.DATA['token']):
				comment = request.DATA['message']
				user = User.objects.get(username=request.DATA['user'])
				if 'receiver' in request.DATA:
					receiver = User.objects.get(username=request.DATA['receiver'])
					message = Message(sender=user,receiver=receiver,message=comment)
					message.save()
				else:
					group = Group.objects.get(slug=request.DATA['group'])
					message = Message(sender=user,receiver=group.administrator,message=comment)
					message.save()
				return Response({'message':True})
			else:
				return Response({'message':False})
		except Exception as e:
			return Response({'message':False})

class InivitationGroupViewSet(viewsets.ViewSet):
	def post(self,request,token=None):
		try:
			if is_session(request.DATA['token']):
				comment = request.DATA['comment']
				user = User.objects.get(username=request.DATA['user'])
				group = Group.objects.get(slug=request.DATA['group'])
				inivitation = InivitationGroup(comment=comment,group=group,user=user)
				inivitation.save()
				notificationInvitationGroup(user,group,group)
				return Response({'invitation':True})
			else:
				return Response({'invitation':False})
		except IntegrityError:
			return Response({'invitation':False})
		except Exception as e:
			print e
			return Response({'invitation':False})

class InivitationFriendViewSet(viewsets.ViewSet):
	def post(self,request,token=None):
		try:
			if is_session(request.DATA['token']):
				comment = request.DATA['comment']
				user = User.objects.get(username=request.DATA['user'])
				friend = User.objects.get(username=request.DATA['sender'])
				invitation = InivitationFriend(friend=friend,comment=comment,user=user)
				invitation.save()
				notificationFriendInvitation(friend,user)
				return Response({'invitation':True})
			else:
				return Response({'invitation':False})
		except IntegrityError:
			return Response({'invitation':False})
		except Exception as e:
			print e
			return Response({'invitation':False})

class ConversationsViewSet(viewsets.ViewSet):
	def list(self,request,session_key,username):
		try:
			if is_session(session_key):
				user = User.objects.get(username=username)
				conversations = Message.objects.getConversations(user)
				serializer = ConversationSerializer(conversations,many=True,context={'request':request})
				return Response({"conversation":True,"conversation":serializer.data})
			else:
				return Response({'conversation':False})
		except Exception as e:
			raise

class MessagesViewSet(viewsets.ViewSet):
	def list(self,request,session_key,username,sender):
		try:
			if is_session(session_key):
				user = User.objects.get(username=username)
				sender = User.objects.get(username=sender)
				messages = Message.objects.getMessages(user,sender)
				Message.objects.updateRead(user,sender)
				serializer = MessagesSerializer(messages,many=True,context={'request':request})
				return Response({"session":True,"messages":serializer.data})
			else:
				return Response({'session':False})
		except Exception as e:
			raise

class ResetPasswordViewSet(viewsets.ViewSet):
	def post(self,request):
		try:
			email = request.DATA['email']
			password_reset(request,email_template_name='account/reset_email.html',html_email_template_name='account/reset_email.html',subject_template_name='account/reset_subject.txt')
			return Response({'reset':True})
		except Exception as e:
			print e
			return Response({'reset':False})

class YoutubeViewSet(viewsets.ViewSet):
	def post(self,request):
		try:
			url_video = request.DATA['url_video']
			ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s%(ext)s'})
			with ydl:
				result = ydl.extract_info(url_video,download=False)
			if 'entries' in result:
				video = result['entries'][0]
			else:
				video = result
			video_url = video['url']
			return Response({'video':True,'url':video_url})
		except Exception as e:
			return Response({'video':False})
