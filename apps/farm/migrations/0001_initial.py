# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Farm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=20)),
                ('web_site', models.URLField()),
                ('openning_date', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FarmProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slogan', models.CharField(max_length=200, null=True, blank=True)),
                ('web_site2', models.URLField(null=True, blank=True)),
                ('facebook', models.CharField(max_length=100, null=True, blank=True)),
                ('twitter', models.CharField(max_length=100, null=True, blank=True)),
                ('google_analytics', models.CharField(max_length=50, null=True, blank=True)),
                ('logo', models.ImageField(default=b'farm_profile/farm_logo.jpg', upload_to=b'farm_profile')),
                ('banner', models.ImageField(default=b'farm_profile/farm_banner.jpg', upload_to=b'farm_profile')),
                ('latitude', models.FloatField(default=1.63789, null=True, blank=True)),
                ('longitude', models.FloatField(default=-77.7452081, null=True, blank=True)),
                ('farm', models.OneToOneField(to='farm.Farm')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('summary', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('quantity', models.SmallIntegerField()),
                ('is_presale', models.BooleanField(default=False)),
                ('presale_deadline', models.DateTimeField(null=True, blank=True)),
                ('image', models.ImageField(default=b'farm_products/product.jpg', upload_to=b'farm_products')),
                ('slug', autoslug.fields.AutoSlugField(editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(default=b'farm_products/product.jpg', upload_to=b'farm_products')),
                ('product', models.ForeignKey(to='farm.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(to='farm.ProductCategory'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='farm',
            field=models.ForeignKey(to='farm.Farm'),
            preserve_default=True,
        ),
    ]
