# coding=utf-8

from django.db import models
from apps.farm.models import Farm
from apps.groups.models import Group
from autoslug import AutoSlugField
from django.db.models import Avg, Count, Sum, Max, Min
from django.core.urlresolvers import reverse

class ProductCategory(models.Model):
    '''This models allows create and update product categories'''
    name=models.CharField(max_length=50)
    slug = AutoSlugField(populate_from='name', unique_with='name', always_update=True)
    image = models.ImageField(upload_to='farm_category', default='farm_category/category.jpg')
    icon = models.ImageField(upload_to='farm_category', default='farm_category/no_image.jpg')
    icon_color = models.ImageField(upload_to='farm_category', default='farm_category/no_image.jpg')

    def __unicode__(self):
        return self.name

    def countProducts(self):
        '''This function counts the products by category'''
        count = Product.objects.filter(is_active=True,category=self).count()
        return count

    def countProductsMeta(self):
        '''This function counts the products by category'''
        count = Product.objects.filter(is_active=True,category=self).count()
        return "Más de {0} productos en {1}".format(count,self.name)

    def getPictureMeta(self):
        '''This function returns an image of a product'''
        image = "/media/{0}".format(self.image)
        return image

class ProductManager(models.Manager):
    '''This manager extends the product model'''
    def count(self):
        count = self.filter(is_active=True).count()
        return count

    def counCategories(self):
        '''This function counts the products by category'''
        categories=self.filter(farm__is_active=True,is_active=True).values('category').annotate(count=Count('category')).order_by('category')
        for category in categories:
            category['category']=ProductCategory.objects.values('name','slug','icon','icon_color').get(pk=category['category'])
        return categories

class Product(models.Model):
    '''This model allows save products'''
    farm=models.ForeignKey(Farm)
    category=models.ForeignKey(ProductCategory)
    name = models.CharField(max_length=50)
    summary = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    quantity = models.SmallIntegerField()
    slug = AutoSlugField(populate_from='name', unique='name',always_update=True)
    is_active = models.BooleanField(default=True)
    objects=ProductManager()

    def __unicode__(self):
        return self.slug

    def get_absolute_url(self):
		return reverse('product', kwargs={'slug':self.slug})

    def getPicture(self):
        '''This function returns an image of a product'''
        images = ProductImage.objects.filter(product=self)
        if not images:
            image='farm_products/no_image.png'
        else:
            image=images[0].image
        return image

    def getPictureMeta(self):
        '''This function returns an image of a product'''
        images = ProductImage.objects.filter(product=self)
        if not images:
            image='/media/farm_products/no_image.png'
        else:
            image="/media/{0}".format(images[0].image)
        return image

    def getAllPicture(self):
        '''This functions returns all image of a product'''
        import json
        images = ProductImage.objects.filter(product=self)
        images_list=""
        if images:
            for img in images:
                images_list+=img.image.name+"@@@$$$###"
        else:
            images_list+='farm_products/no_image.png'+"@@@$$$###"
        return images_list

    def getAllPicture2(self):
        '''This functions returns all image of a product'''
        images = ProductImage.objects.filter(product=self)
        return images

    def getFeedback(self):
        '''This function returns the feedback from a product'''
        from apps.store.models import FeedbackProduct
        feedback=FeedbackProduct.objects.filter(order__product=self).aggregate(price=Avg('price'),quality=Avg('quality'),description=Avg('description'),count=Count('order__product'))
        if feedback['count']>0:
            total=(feedback['price']+feedback['quality']+feedback['description'])/3
        else:
            feedback['total']=0
            feedback['price']=0
            feedback['quality']=0
            feedback['description']=0
        return feedback

class ProductImage(models.Model):
    '''This model allows save pictures a product'''
    product=models.ForeignKey(Product)
    image = models.ImageField(upload_to='farm_products',default='farm_products/product.jpg')

    def __unicode__(self):
    	return self.product.name

class ProductsGroup(models.Model):
    '''This model allows add product to group'''
    product = models.ForeignKey(Product)
    group = models.ForeignKey(Group)

    class Meta:
        unique_together=(('group','product'),)

    def __unicode__(self):
        return self.product.name

def haveProductsFarm(user):
    '''This function checks if the farm have products'''
    haveProducts=Product.objects.filter(farm__user=user)
    if haveProducts:
        return True
    else:
        return False
