from apps.farm.models import Farm, FarmProfile
from apps.product.models import Product, ProductCategory
from apps.account.models import Profile, getUserFullName
from apps.groups.models import GroupMember
from apps.message.models import Message
from apps.comments.models import Comment
from apps.blog.models import Category
from apps.store.models import ProductComments
from django.db.models import Q

def globalVars(request):
	if request.user.is_authenticated():
		dic={'haveFarm':haveFarm(request.user),
		'farm_admin':getFarmAdmin(request.user),
		'full_name':getUserFullName(request.user),
		'user_profile':getUserProfile(request.user),
		'count_comments':countCommentsNoRead(request.user),
		'farm_profile':getFarmProfileAdmin(request.user),
		'farmIsActive':farmIsActive(request.user),
		'allGroups':getAllGroupsUser(request.user),
		'unread_messages':Message.objects.countUnread(request.user),
		'ads':getAds(),
		'blog_categories':blogCategories(),
		'product_categories':productCategories()}
	else:
		dic={'none':'none',
		'ads':getAds(),
		'blog_categories':blogCategories(),
		'product_categories':productCategories()}
	return dic

def haveFarm(user):
	try:
		farm=Farm.objects.get(user=user)
		return True
	except Farm.DoesNotExist:
		return False

def getAds():
	return Product.objects.filter(is_active=True).order_by('?')[:3]

def getFarmUser(user):
	try:
		farm=Farm.objects.get(user=user)
		return farm
	except Farm.DoesNotExist:
		return False

def farmIsActive(user):
	try:
		farm=Farm.objects.get(user=user)
		return farm.is_active
	except Farm.DoesNotExist:
		return False

def getUserProfile(user):
	try:
		profile=Profile.objects.get(user=user)
		return profile
	except:
		return False

def getFarmAdmin(user):
	try:
		farm=Farm.objects.get(user=user)
		return farm
	except Farm.DoesNotExist:
		return False

def getAllGroupsUser(user):
	try:
		groups=GroupMember.objects.filter(user=user)
		return groups
	except GroupMember.DoesNotExist:
		return False

def getActiveGroupsUser(user):
	try:
		groups=GroupMember.objects.filter(user=user,group__is_active=True)
		return groups
	except GroupMember.DoesNotExist:
		return False

def getFarmProfileAdmin(user):
	try:
		farm=Farm.objects.get(user=user)
		profile=FarmProfile.objects.get(farm=farm)
		return profile
	except Farm.DoesNotExist:
		return False

def countCommentsNoRead(user):
	try:
		comments=ProductComments.objects.filter(Q(seller=user) | Q(buyer=user),is_read=False).count()
		return comments
	except ProductComments.DoesNotExist:
		return False

def blogCategories():
	categories = Category.objects.menuCategory()
	return categories

def productCategories():
	categories = ProductCategory.objects.all().order_by('name')
	return categories
