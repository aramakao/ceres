# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_productsgroup'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='productsgroup',
            unique_together=set([('group', 'product')]),
        ),
    ]
