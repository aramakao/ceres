# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0008_auto_20150730_2047'),
    ]

    operations = [
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
    ]
