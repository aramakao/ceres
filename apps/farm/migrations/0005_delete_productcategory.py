# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0004_productcategory_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductCategory',
        ),
    ]
