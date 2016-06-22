from apps.account.models import User, Profile, StateUserComment, Friend, StateUser
from apps.product.models import Product, ProductCategory, ProductImage
from apps.store.models import *
from apps.message.models import *
from apps.farm.models import Farm, FarmProfile
from apps.blog.models import Blog, Category
from apps.meter.models import *
from apps.search.models import Index
from apps.groups.models import *
from rest_framework import serializers
from apps.ceres.processors import getUserFullName

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username','avatar','fullName')
        read_only = True

class UserMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','avatar','fullName')
        read_only = True

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ('title','slug','image')

class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = ('name','slug','logo','address','phone')

class FarmProfileMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmProfile
        fields = ('slogan','banner')

class FarmMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = ('name','slug','logo')

class CategorySummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('name','slug')

class ProductMinSerializer(serializers.ModelSerializer):
    farm = FarmMinSerializer(many=False)
    category = CategorySummarySerializer()
    getPicture = serializers.CharField()
    class Meta:
        model = Product
        fields = ('farm','name','slug','price','quantity','getPicture', 'category')
        read_only = True

class ProductWithoutFarmSerializer(serializers.ModelSerializer):
    category = CategorySummarySerializer()
    getPicture = serializers.CharField()
    class Meta:
        model = Product
        fields = ('name','slug','price','quantity','getPicture', 'category')
        read_only = True

class FriendSerializer(serializers.ModelSerializer):
    friend = UserMinSerializer(many=False,read_only=True)
    date_since = serializers.CharField()
    class Meta:
        model = Friend
        fields = ('friend','date_since')

class UserProfileMinSerializer(serializers.ModelSerializer):
    user = UserMinSerializer(many=False,read_only=True)
    get_occupation = serializers.CharField()
    get_phone = serializers.CharField()
    class Meta:
        model = Profile
        fields = ('user','get_occupation','get_phone','banner')

class StateUserSerializer(serializers.ModelSerializer):
    count_comments = serializers.IntegerField()
    date_since = serializers.CharField()
    class Meta:
        model = StateUser

class StateSerializer(serializers.ModelSerializer):
    count_comments = serializers.IntegerField()
    date_since = serializers.CharField()
    user = UserMinSerializer()
    class Meta:
        model = StateUser
        fields = ('id','count_comments','date_since','text','user')


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserMinSerializer(many=False,read_only=True)
    get_farm=FarmSerializer(many=False,read_only=True)
    get_states = StateUserSerializer(many=True,read_only=True)
    get_occupation = serializers.CharField()
    get_phone = serializers.CharField()
    class Meta:
        model = Profile

class FarmProfileSerializer(serializers.ModelSerializer):
    farm=FarmSerializer(many=False,read_only=True)
    profile = UserProfileMinSerializer(many=False,read_only=True)
    products = ProductWithoutFarmSerializer(many=True,read_only=True)
    class Meta:
        model = FarmProfile
        fields = ('farm','slogan','banner','latitude','longitude','location','profile','products')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory

class CategoryMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('name','slug','icon','icon_color')

class ProductPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage

class GeoFarmsCountCitySerializer(serializers.Serializer):
    count = serializers.IntegerField()
    location = serializers.CharField(max_length=100)
    location_slug = serializers.CharField(max_length=100)

class ProductSerializer(serializers.ModelSerializer):
    farm = FarmMinSerializer(many=False,read_only=True)
    category = CategorySummarySerializer(many=False,read_only=True)
    getPicture = serializers.CharField()
    getAllPicture = serializers.CharField()
    getFeedback = serializers.CharField()
    class Meta:
	    model = Product
	    fields = ('farm', 'category',
        'name', 'slug', 'price', 'quantity',
        'summary', 'getPicture','description',
        'getAllPicture','getFeedback')

class CategoryBlogMinSerializar(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name','slug')

class EntryMinSerializar(serializers.ModelSerializer):
    category = CategoryBlogMinSerializar(many=False,read_only=True)
    minContent = serializers.CharField()
    date_post = serializers.CharField()
    class Meta:
        model = Blog
        fields = ('title','slug','category','minContent','image','date_post')


class EntrySerializar(serializers.ModelSerializer):
    category = CategoryBlogMinSerializar(many=False,read_only=True)
    date_post = serializers.CharField()
    class Meta:
        model = Blog
        fields = ('title','slug','category','content','image','date_post')

class LatestProductSerializer(serializers.ModelSerializer):
    farm = FarmMinSerializer(many=False)
    category = CategorySummarySerializer()
    getPicture = serializers.CharField()
    class Meta:
        model = Product
        fields = ('farm','name','slug','price','quantity','getPicture', 'category')
        read_only = True

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name','logo','phone','address','slug')
        read_only = True

class GroupProfileSerializer(serializers.ModelSerializer):
    group = GroupSerializer(many=False)
    class Meta:
        model = GroupProfile
        read_only = True

class GroupsUserSerializer(serializers.ModelSerializer):
    group = GroupSerializer(many=False,read_only=True)
    #date_since = serializers.CharField()
    class Meta:
        model = GroupMember
        #fields = ('friend','date_since')


class GroupMemberSerializer(serializers.ModelSerializer):
    user = UserMinSerializer(many=False,read_only=True)
    date_since = serializers.CharField()
    class Meta:
        model = GroupMember
        read_only = True

class CategoryProductSerializer(serializers.ModelSerializer):
    countProducts = serializers.IntegerField()
    class Meta:
        model = ProductCategory

class StatusCommentsSerializer(serializers.ModelSerializer):
    user = UserMinSerializer(many=False,read_only=True)
    date_post=serializers.CharField(max_length=20)
    class Meta:
        model = StateUserComment

class StateCommentsSerializer(serializers.ModelSerializer):
    user = UserMinSerializer(many=False,read_only=True)
    date_post = serializers.CharField()
    class Meta:
        model = StateUserComment
        fields = ('user','date_post','text','picture','id')

class StatusGroupCommentsSerializer(serializers.ModelSerializer):
    user = UserMinSerializer(many=False,read_only=True)
    date_post=serializers.CharField(max_length=20)
    class Meta:
        model = StateUserComment

class IndexMinSerializer(serializers.Serializer):
    text = serializers.CharField()
    url = serializers.URLField()
    image = serializers.URLField()
    source= serializers.CharField()
    slug= serializers.CharField()

class ShoppingCartSerializer(serializers.Serializer):
    product_slug=serializers.CharField()
    farm_slug=serializers.CharField()
    image=serializers.CharField()
    price=serializers.FloatField(max_value=None, min_value=None)
    subtotal=serializers.CharField()
    farm=serializers.CharField()
    product_name=serializers.CharField()
    n_quantity=serializers.IntegerField()
    shipping_price=serializers.CharField()
    shipping=serializers.CharField()
    shipping_id=serializers.IntegerField()

class QuestionSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Question

class MainSerializer(serializers.Serializer):
    banners =BannerSerializer(many=True,read_only=True)
    products = ProductMinSerializer(many=True, read_only=True)
    #image = serializers.CharField()

class GeoFarmSerializar(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    farm__name = serializers.CharField()
    slogan = serializers.CharField()
    farm__slug = serializers.CharField()

class MailboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mailbox

class FeedbackProductSerializer(serializers.ModelSerializer):
    date_post = serializers.CharField()
    class Meta:
        model = FeedbackProduct
        fields = ('comment','price','quality','description','date_post')

class ProductCommentsSerializer(serializers.ModelSerializer):
    buyer = UserMinSerializer()
    seller = UserMinSerializer()
    date_ask = serializers.CharField()
    date_reply = serializers.CharField()

    class Meta:
        model = ProductComments
        fields = ('id','buyer','seller','date_ask','date_reply','ask','reply','is_read')

class ShippingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingOption

class PaymentOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id','description','get_payment_display')

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress

class ConversationSerializer(serializers.ModelSerializer):
    sender = UserMinSerializer()
    icon = serializers.CharField()
    timesince = serializers.CharField()
    class Meta:
        model = Message
        fields = ('sender','icon','message','timesince')

class MessagesSerializer(serializers.ModelSerializer):
    is_receiver = serializers.BooleanField()
    timesince = serializers.CharField()
    class Meta:
        model = Message
        fields = ('message','timesince','is_receiver')
