# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_productcomments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productcomments',
            name='buyer',
        ),
        migrations.RemoveField(
            model_name='productcomments',
            name='product',
        ),
        migrations.RemoveField(
            model_name='productcomments',
            name='seller',
        ),
        migrations.DeleteModel(
            name='ProductComments',
        ),
    ]
