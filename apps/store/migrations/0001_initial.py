# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0015_auto_20150710_0343'),
        ('product', '0010_auto_20150804_0645'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Advert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_post', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(default=b'adverts/adverts.jpg', upload_to=b'adverts')),
                ('summary', models.TextField()),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from=b'summary', always_update=True, unique=b'summary')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FeedbackBuyer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField()),
                ('communication', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('responsibility', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('friendliness', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FeedbackProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField()),
                ('quality', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('description', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FeedbackSeller',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('observations', models.TextField()),
                ('communication', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('quickness', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('responsibility', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('payment', models.IntegerField(default=2, choices=[(1, b'Efectivo'), (2, b'Acordar con el Vendedor'), (3, b'Giros'), (4, b'Consignaci\xc3\xb3n Bancaria'), (5, b'Contra Entrega')])),
                ('description', models.TextField()),
                ('farm', models.ForeignKey(to='farm.Farm')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductComments',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_post_ask', models.DateTimeField(auto_now_add=True)),
                ('date_post_reply', models.DateTimeField(null=True, blank=True)),
                ('ask', models.TextField()),
                ('reply', models.TextField(null=True, blank=True)),
                ('is_read', models.BooleanField(default=False)),
                ('buyer', models.ForeignKey(related_name='custom_buyer_comment', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(to='product.Product')),
                ('seller', models.ForeignKey(related_name='custom_seller_comment', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField(default=0)),
                ('shipping', models.TextField()),
                ('total', models.FloatField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('state', models.IntegerField(default=1, choices=[(1, b'Pedido'), (2, b'Enviado'), (3, b'Finalizado'), (4, b'Cancelado')])),
                ('received', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PurchaseRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.IntegerField(default=1, choices=[(1, b'Realiz\xc3\xb3 una Compra'), (2, b'Nuevo Estado'), (3, b'Notificaci\xc3\xb3n Cliente'), (4, b'Notificaci\xc3\xb3n Vendedor')])),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('detail', models.TextField()),
                ('purchase_order', models.ForeignKey(to='store.PurchaseOrder')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShippingAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('neighborhood', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShippingOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('detail', models.TextField()),
                ('price', models.FloatField(default=0)),
                ('porcentage', models.FloatField(default=0)),
                ('farm', models.ForeignKey(to='farm.Farm')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField()),
                ('product', models.ForeignKey(to='product.Product')),
                ('shipping', models.ForeignKey(blank=True, to='store.ShippingOption', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='shoppingcart',
            unique_together=set([('user', 'product')]),
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='address',
            field=models.ForeignKey(to='store.ShippingAddress'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='buyer',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='farm',
            field=models.ForeignKey(to='farm.Farm'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='payment',
            field=models.ForeignKey(to='store.Payment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='productorder',
            name='order',
            field=models.ForeignKey(to='store.PurchaseOrder'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='productorder',
            name='product',
            field=models.ForeignKey(to='product.Product'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='payment',
            unique_together=set([('payment', 'farm')]),
        ),
        migrations.AddField(
            model_name='feedbackseller',
            name='order',
            field=models.OneToOneField(to='store.PurchaseOrder'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='feedbackproduct',
            name='order',
            field=models.ForeignKey(to='store.PurchaseOrder'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='feedbackbuyer',
            name='order',
            field=models.OneToOneField(to='store.PurchaseOrder'),
            preserve_default=True,
        ),
    ]
