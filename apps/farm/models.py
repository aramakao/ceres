#-*- encoding: utf-8 -*-
from django.db import models
from apps.account.models import User
from autoslug import AutoSlugField
from apps.extras.models import Region, City
from django.core.urlresolvers import reverse

class FarmManager(models.Manager):
	'''This manager allows extends the model farm'''

	def create_farm(self,name,address,phone,user):
		'''This function create a farm with the profile'''
		farm = self.create(name=name,address=address,phone=phone,user=user)
		profile = FarmProfile(farm=farm)
		profile.save()
		return farm

class Farm(models.Model):
	'''This model allows create farms'''
	name = models.CharField(null=False, max_length=50, unique=True)
	address = models.CharField(null=False, max_length=50)
	phone = models.CharField(max_length=20)
	logo = models.ImageField(upload_to='farm_profile', default='farm_profile/farm_logo.jpg')
	slug = AutoSlugField(populate_from='name', unique_with='name', always_update=True)
	user= models.OneToOneField(User)
	openning_date = models.DateTimeField(auto_now_add=True)
	is_active=models.BooleanField(default=True)
	objects = FarmManager()

	def __unicode__(self):
		return self.name
		
	def save(self,*args,**kwargs):
		'''This function creates a farm with profile, shipping and payment setup'''
		if not self.pk:
			from apps.store.models import ShippingOption,Payment
			super(Farm,self).save(*args, **kwargs)
			profile = FarmProfile(farm=self)
			profile.save()
			shipping = ShippingOption(farm=self,name='Acordar con el vendedor',detail='Opción generada por el sistema')
			shipping.save()
			payment = Payment(farm=self,description='Opción generada por el sistema')
			payment.save()
		else:
			super(Farm,self).save(*args, **kwargs)
		return self

	def get_absolute_url(self):
		return reverse('farm', kwargs={'farm':self.slug})

	def get_last_products(self):
		'''This functions returns the last ten products'''
		from apps.product.models import Product
		products = Product.objects.filter(farm=self,is_active=True)[:10]
		return products

class FarmProfile(models.Model):
	'''This model allows create a farm profile'''
	farm=models.OneToOneField(Farm)
	slogan = models.CharField(blank=True,max_length=200,null=True)
	facebook = models.CharField(max_length=100,blank=True,null=True)
	twitter = models.CharField(max_length=100,blank=True,null=True)
	web_site = models.CharField(max_length=100,blank=True,null=True)
	banner = models.ImageField(upload_to='farm_profile', default='farm_profile/farm_banner.jpg')
	latitude = models.FloatField(null=True,blank=True,default=1.63789)
	longitude = models.FloatField(null=True, blank=True, default=-77.7452081)
	location = models.CharField(blank=True,max_length=200,null=True)
	location_slug = AutoSlugField(populate_from='location', always_update=True)

	def __unicode__(self):
		return self.farm.name

	def get_slogan(self):
		'''This function return the slogan'''
		if self.slogan:
			return self.slogan
		else:
			return 'Desconocido'
