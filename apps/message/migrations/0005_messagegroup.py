# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0010_inivitationgroup_date'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('message', '0004_message_is_read'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('message', models.CharField(max_length=200)),
                ('file', models.FileField(null=True, upload_to=b'messages', blank=True)),
                ('receiver', models.ForeignKey(to='groups.Group')),
                ('sender', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
