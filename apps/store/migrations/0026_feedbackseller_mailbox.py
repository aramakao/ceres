# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0025_auto_20151118_0100'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedbackSeller',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('observations', models.TextField()),
                ('communication', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('quickness', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('responsibility', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('reply', models.TextField(null=True, blank=True)),
                ('order', models.OneToOneField(to='store.PurchaseOrder')),
            ],
        ),
        migrations.CreateModel(
            name='Mailbox',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.CharField(max_length=50, blank=True)),
                ('phone', models.CharField(max_length=50, blank=True)),
                ('email', models.CharField(max_length=100, blank=True)),
                ('message', models.TextField()),
                ('reply', models.TextField(null=True, blank=True)),
            ],
        ),
    ]
