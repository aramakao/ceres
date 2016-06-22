# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_blog_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='in_banner',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
