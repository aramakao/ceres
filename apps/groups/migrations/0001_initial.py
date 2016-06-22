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
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('slug', autoslug.fields.AutoSlugField(always_update=True, populate_from=b'name', unique_with=(b'name',), editable=False)),
                ('openning_date', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('administrator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slogan', models.CharField(max_length=200, null=True, blank=True)),
                ('logo', models.ImageField(default=b'group_profile/group_logo.jpg', upload_to=b'farm_profile')),
                ('banner', models.ImageField(default=b'group_profile/group_banner.jpg', upload_to=b'farm_profile')),
                ('latitude', models.FloatField(default=1.63789, null=True, blank=True)),
                ('longitude', models.FloatField(default=-77.7452081, null=True, blank=True)),
                ('location', models.CharField(max_length=200, null=True, blank=True)),
                ('location_slug', autoslug.fields.AutoSlugField(always_update=True, populate_from=b'location', editable=False)),
                ('group', models.OneToOneField(to='groups.Group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
