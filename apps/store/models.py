#-*- encoding: utf-8 -*-
from django.db import models
from django.db.models import Avg, Count, Sum, Max, Min
from apps.product.models import Product
from apps.account.models import User
from apps.farm.models import Farm
from autoslug import AutoSlugField
from apps.ceres.notification import notificationShop
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import *
from calendar import Calendar
import datetime
from django.utils.timesince import timesince
from django.db.models import Q

class ProductCommentsManager(models.Manager):
	'''This manager allows extends the product comments model'''
	def getComments(self,user):
		comments = self.filter(Q(seller = user) | Q( buyer = user)).order_by('-date_post_ask')
		return comments

class ProductComments(models.Model):
	'''This model allows write comments to product'''
	date_post_ask = models.DateTimeField(auto_now_add=True)
	date_post_reply = models.DateTimeField(blank=True,null=True)
	product=models.ForeignKey(Product)
	buyer=models.ForeignKey(User, related_name="custom_buyer_comment")
	seller=models.ForeignKey(User, related_name="custom_seller_comment")
	ask = models.TextField()
	reply = models.TextField(blank=True,null=True)
	is_read = models.BooleanField(default=False)
	objects = ProductCommentsManager()

	def __unicode__(self):
		return self.ask

	def date_ask(self):
		'''This function returns the date asking'''
		return "Hace "+ timesince(self.date_post_ask)

	def date_reply(self):
		'''This function returns the date reply'''
		if self.date_post_reply:
			return "Hace "+ timesince(self.date_post_reply)
		else:
			return False

		return '%s' %(self.user)

PAYMENTS_CHOICES = (
    (1, 'Efectivo'),
    (2, 'Acordar con el Vendedor'),
    (3, 'Giros'),
	(4, 'Consignación Bancaria'),
	(5, 'Contra Entrega'),
)
class Payment(models.Model):
	'''This model allows create pyament options'''
	payment=models.IntegerField(choices=PAYMENTS_CHOICES,default=2)
	farm=models.ForeignKey(Farm)
	description = models.TextField()

	class Meta:
		unique_together=(('payment','farm'),)

	def __unicode__(self):
		return self.farm.name

class ShippingOption(models.Model):
	'''This model allows create shipping options'''
	farm = models.ForeignKey(Farm)
	name = models.CharField(max_length=50)
	detail = models.TextField()
	price = models.FloatField(default=0)
	porcentage = models.FloatField(default=0)

	def __unicode__(self):
		return self.detail

class ShippingAddress(models.Model):
	'''This model allows save the shipping address'''
	user = models.OneToOneField(User)
	neighborhood = models.CharField(max_length=50)
	address = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	phone = models.CharField(max_length=20)
	description = models.TextField()

	def __unicode__(self):
		return self.address

class PurchaseOrderManager(models.Manager):
	'''This manager allows extend the purchase order model'''
	def create_order(self,product,shipping_option,quantity,payment_id,user,address):
		'''This function allows create a new order'''
		if shipping_option.price:
			total = Decimal(quantity)*(Decimal(shipping_option.price)+Decimal(product.price))
			shipping="{}. Descripción: El envío tiene un valor fijo de ${}".format(shipping_option.name,shipping_option.price)
		else:
			total = Decimal(quantity)*((Decimal(shipping_option.price)*Decimal(product.price))+Decimal(product.price))
			shipping="{}. Descripción: El envío tiene un valor variable del {}% con respecto al valor del producto".format(shipping_option.name,shipping_option.porcentage)
		order = PurchaseOrder(buyer=user,farm=product.farm,address=address,payment_id=payment_id,product=product,quantity=quantity,price=product.price,shipping=shipping,total_order=total)
		order.save()
		PurchaseRecord(purchase_order=order,detail="Se ha realizado la compra de {}".format(product.name)).save()
		notificationShop(user,product.farm.user,order)
		return order

	def month_sales(self,farm):
		'''This function returns the monthly sales'''
		date = datetime.date.today()
		cal = Calendar()
		days_month=list(set(list(cal.itermonthdays(date.year, date.month)))-set([0]))
		orders = PurchaseOrder.objects.filter(farm=farm,date__month=date.month,date__year=date.year)
		products=PurchaseOrder.objects.product_order_month(farm,date)
		total_day=[]
		count_sales=[]
		for day in days_month:
			total_day.append(0)
			count_sales.append(0)
		total_month=0
		total_products = PurchaseOrder.objects.count_products_month(farm,date)
		for order in orders:
			for idx,day in enumerate(days_month):
				if order.date.day==day:
					total = order.total_order
					t_products = order.quantity
					if total_day[idx]!=0:
						price  = total_day[idx]+total
						total_day[idx]=price
						total_month+=total
						count = count_sales[idx]
						count_sales[idx]=(count+t_products)
					else:
						total_month+=total
						total_day[idx]=total
						count_sales[idx]=(t_products)

					break
		data = {'labels':days_month, 'values':total_day, 'count':count_sales, 'total_month':total_month, 'total_products':total_products, 'products':products}
		return data

	def day_sales(self,farm):
		'''This function returns the daily sales'''
		date = datetime.date.today()
		hours = [[0,4],[4,8],[8,12],[12,16],[16,20],[20,24]]
		total_hours=[]
		count_sales=[]
		for hour in hours:
			total_hours.append(0)
			count_sales.append(0)
		products=PurchaseOrder.objects.product_order_day(farm,date)
		total_products = PurchaseOrder.objects.count_products_day(farm,date)
		total_day=0
		orders = PurchaseOrder.objects.filter(farm=farm, date__month=date.month, date__day=date.day)
		for order in orders:
			for idx,hour in enumerate(hours):
				if order.date.hour in range(hour[0],hour[1]):
					total = order.total_order
					t_products = order.quantity
					if total_hours[idx]!=0:
						price  = total_hours[idx]+total
						total_hours[idx]=price
						total_day+=total
						count = count_sales[idx]
						count_sales[idx]=(count+t_products)
					else:
						total_day+=total
						total_hours[idx]=total_day
						count_sales[idx]=(t_products)
					break
		data = {'values':total_hours, 'count':count_sales, 'total_day':total_day, 'total_products':total_products, 'products':products}
		return data

	def week_sales(self,farm):
		'''This function returns the weekly deals'''
		date = datetime.date.today()
		orders = PurchaseOrder.objects.order_week(farm=farm,date=date)
		products_order=PurchaseOrder.objects.product_order_week(farm=farm,orders=orders)
		total_products = products_order[0]['total']
		products = products_order[1]
		sales_day=[]
		count_sales=[]
		total_day=0
		cal = Calendar()
		days = list(cal.iterweekdays())
		for day in days:
			sales_day.append(0)
			count_sales.append(0)
		for order in orders:
			order_day=order.date.isocalendar()[2]
			total = order.total_order
			t_products = order.quantity
			for day in days:
				if day==order_day:
					if sales_day[day]!=0:
						price  = sales_day[day]+total
						sales_day[day]=price
						total_day+=total
						count = count_sales[day]
						count_sales[day]=(count+t_products)
					else:
						total_day+=total
						sales_day[day]=total_day
						count_sales[day]=(t_products)
					break
		data = {'values':sales_day, 'count':count_sales, 'total_day':total_day, 'total_products':total_products, 'products':products}
		return data

	def year_sales(self,farm):
		'''This function returns the annual sales'''
		date = datetime.date.today()
		months_year=[]
		for month in range(1,13):
			months_year.append(month)
		orders = PurchaseOrder.objects.filter(farm=farm, date__year=date.year)
		products=PurchaseOrder.objects.product_order_year(farm,date)
		sales_month=[]
		count_sales=[]
		for day in months_year:
			sales_month.append(0)
			count_sales.append(0)
		total_year=0
		total_products = PurchaseOrder.objects.count_products_year(farm,date)
		for order in orders:
			for idx,month in enumerate(months_year):
				if order.date.month==month:
					total = order.total_order
					t_products = order.quantity
					if sales_month[idx]!=0:
						price  = sales_month[idx]+total
						sales_month[idx]=price
						total_year+=total
						count = count_sales[idx]
						count_sales[idx]=(count+t_products)
					else:
						total_year+=total
						sales_month[idx]=total
						count_sales[idx]=(t_products)
					break
		data = {'values':sales_month, 'count':count_sales, 'total_year':total_year, 'total_products':total_products, 'products':products}
		return data

	def origin_sales(self,farm):
		'''This fucntion returns the sales since the farm opened'''
		orders = PurchaseOrder.objects.filter(farm=farm)
		rang=PurchaseOrder.objects.aggregate(Max('date'), Min('date'))
		years=[]
		for year in range(rang['date__min'].year,rang['date__max'].year+1):
			years.append(year)
		products=PurchaseOrder.objects.product_order_origin(farm)
		sales_year=[]
		count_sales=[]
		for day in years:
			sales_year.append(0)
			count_sales.append(0)
		total_year=0
		total_products = PurchaseOrder.objects.total(farm)
		for order in orders:
			for idx,year in enumerate(years):
				if order.date.year==year:
					total = order.total_order
					t_products = order.quantity
					if sales_year[idx]!=0:
						price  = sales_year[idx]+total
						sales_year[idx]=price
						total_year+=t_products
						count = count_sales[idx]
						count_sales[idx]=(count+t_products)
					else:
						total_year+=t_products
						sales_year[idx]=total
						count_sales[idx]=(t_products)
					break
		data = {'values':sales_year,'labels':years, 'count':count_sales, 'products':products, 'total_products':total_year}
		return data

	def order_week(self,farm,date):
		'''This function returns the sales were made in week'''
		orders=PurchaseOrder.objects.filter(farm=farm,date__month=date.month,date__year=date.year)
		orders_week=[]
		for order in orders:
			if date.isocalendar()[1] == order.date.isocalendar()[1]:
				orders_week.append(order)
		return orders_week

	def product_order_week(self,farm,orders):
		'''This function counts the products that sales were sold in week'''
		products=[]
		total={'total':0}
		for order in orders:
			total=PurchaseOrder.objects.filter(farm=farm).aggregate(total=Sum('quantity'))
			products=PurchaseOrder.objects.values('product__name').filter(farm=farm).annotate(count=Sum('quantity'))
		products_order=[]
		products_order.append(total)
		products_order.append(products)
		return products_order

	def product_order_month(self,farm,date):
		'''This function counts the products that were sold in the month'''
		products=PurchaseOrder.objects.values('product__name').annotate(count=Sum('quantity')).filter(farm=farm,date__month=date.month,date__year=date.year)
		return products

	def product_order_year(self,farm,date):
		'''This function counts the products that were sold in the year'''
		products=PurchaseOrder.objects.values('product__name').annotate(count=Sum('quantity')).filter(farm=farm, date__year=date.year)
		return products

	def product_order_origin(self,farm):
		'''This function counts the products that were sold since the farm opened'''
		products=PurchaseOrder.objects.values('product__name').annotate(count=Sum('quantity')).filter(farm=farm)
		return products

	def product_order_day(self,farm,date):
		'''This function counts the products that were sold in the day'''
		products=PurchaseOrder.objects.values('product__name').annotate(count=Sum('quantity')).filter(farm=farm, date__month=date.month, date__day=date.day, date__year=date.year)
		return products

	def total(self,farm):
		'''This function returns the total sales'''
		total_order=PurchaseOrder.objects.filter(farm=farm).aggregate(total=Sum('total_order'))
		return total_order['total']

	def count_products_month(self,farm,date):
		'''This function counts the products that were sold in the month'''
		count = PurchaseOrder.objects.filter(farm=farm, date__month=date.month, date__year=date.year).aggregate(total=Sum('quantity'))
		if not count['total']:
			count['total'] = 0
		return count['total']

	def count_products_year(self,farm,date):
		'''This function counts the products that were sold in the year'''
		count = PurchaseOrder.objects.filter(farm=farm, date__year=date.year).aggregate(total=Sum('quantity'))
		if not count['total']:
			count['total'] = 0
		return count['total']

	def count_products_day(self,farm,date):
		'''This function counts the products that were sold in the day'''
		count = PurchaseOrder.objects.filter(farm=farm, date__month=date.month, date__day=date.day, date__year=date.year).aggregate(total=Sum('quantity'))
		if not count['total']:
			count['total'] = 0
		return count['total']

STATE_ORDER_CHOICES = (
    (1, 'Pedido'),
    (2, 'Enviado'),
    (3, 'Finalizado'),
	(4, 'Cancelado'),
)
class PurchaseOrder(models.Model):
	'''This models allows create purchase orders'''
	date=models.DateTimeField(auto_now_add=True)
	buyer= models.ForeignKey(User)
	farm = models.ForeignKey(Farm)
	state=models.IntegerField(choices=STATE_ORDER_CHOICES,default=1)
	address = models.ForeignKey(ShippingAddress)
	payment = models.ForeignKey(Payment)
	product = models.ForeignKey(Product)
	quantity = models.IntegerField()
	price = models.FloatField(default=0)
	shipping = models.TextField()
	total_order = models.FloatField(default=0)
	received = models.BooleanField(default=False)
	objects = PurchaseOrderManager()

	def __unicode__(self):
		return str(self.id)

	def total_shipping(self):
		'''This function returns the total shipping'''
		return (self.total_order-self.price)

	def total2(self):
		'''This function returns the total price of the order'''
		products = ProductOrder.objects.filter(order=self)
		total_product = 0
		for product in products:
			total_product+=(product.price*product.quantity)
		total = ProductOrder.objects.filter(order=self).aggregate(total=Sum('total'))
		total_shipping = total['total']-total_product
		total['total_shipping']=total_shipping
		total['total_products']=total_product
		return total

	def products(self):
		'''This function returns the products'''
		return ProductOrder.objects.filter(order=self)

	def records(self):
		'''This function returns the purchase order records'''
		return PurchaseRecord.objects.filter(purchase_order=self).order_by('-date')


class ProductOrderManager(models.Manager):
	def create_product(self,products,order,buyer):
		for product in products:
			total = 0
			shipping = ""
			receiver = product.product.farm.user
			if product.shipping.price:
				total = Decimal(product.quantity)*(Decimal(product.shipping.price)+Decimal(product.product.price))
				shipping="{}. Descripción: El envío tiene un valor fijo de ${}".format(product.shipping.name,product.shipping.price)
			else:
				total = Decimal(product.quantity)*((Decimal(product.shipping.price)*Decimal(product.product.price))+Decimal(product.product.price))
				shipping="{}. Descripción: El envío tiene un valor variable del {}% con respecto al valor del producto".format(product.shipping.name,product.shipping.porcentage)
			self.create(order=order, product=product.product, quantity=product.quantity, price=product.product.price, total=total, shipping=shipping)
			product.delete()
		notificationShop(buyer,receiver,order)

PURSCHASE_STATE_CHOICES = (
    (1, 'Realizó una Compra'),
    (2, 'Nuevo Estado'),
    (3, 'Notificación Cliente'),
	(4, 'Notificación Vendedor'),
)

class PurchaseRecord(models.Model):
	purchase_order = models.ForeignKey(PurchaseOrder)
	state = models.IntegerField(choices=PURSCHASE_STATE_CHOICES,default=1)
	date = models.DateTimeField(auto_now_add=True)
	detail = models.TextField()

	def __unicode__(self):
		return self.detail

class FeedbackProduct(models.Model):
	'''This model allows add a comment to product'''
	order = models.OneToOneField(PurchaseOrder)
	date = models.DateTimeField(auto_now_add=True)
	comment = models.TextField()
	quality = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
	description = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
	price = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

	def __unicode__(self):
		return self.order.product.name

	def date_post(self):
		'''This function returns the date post'''
		if self.date:
			return "Hace "+ timesince(self.date)
		else:
			return False

class FeedbackSeller(models.Model):
	'''This model allows feedback to the seller'''
	order = models.OneToOneField(PurchaseOrder)
	date = models.DateTimeField(auto_now_add=True)
	observations = models.TextField()
	communication = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
	quickness = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
	responsibility = models.SmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
	reply = models.TextField(null=True,blank=True)

	def __unicode__(self):
		return self.order.buyer.username

class Mailbox(models.Model):
	'''This model allows write comments about the AgroCeres'''
	date=models.DateTimeField(auto_now_add=True)
	user= models.CharField(max_length=50,blank=True)
	phone=models.CharField(max_length=50,blank=True)
	email=models.CharField(max_length=100,blank=True)
	message=models.TextField()
	reply=models.TextField(null=True,blank=True)

	def __unicode__(self):
		return self.message

def getFeedbackProduct(product):
	'''This function get the feedback from a product'''
	feedback=FeedbackProduct.objects.filter(order__product=product).aggregate(price=Avg('price'),quality=Avg('quality'),description=Avg('description'),count=Count('order__product'))
	if feedback['count']>0:
		total=(feedback['price']+feedback['quality']+feedback['description'])/3
	else:
		total = 0
	feedback['total']=total
	return feedback

def getFeedbackFarm(farm):
	'''This function get the feedback from a farm'''
	feedback=FeedbackSeller.objects.filter(order__farm=farm).aggregate(communication=Avg('communication'),quickness=Avg('quickness'),responsibility=Avg('responsibility'),count=Count('order__farm'))
	if feedback['count']>0:
		total=(feedback['communication']+feedback['quickness']+feedback['responsibility'])/3
	else:
		total = 0
	feedback['total']=total
	return feedback
