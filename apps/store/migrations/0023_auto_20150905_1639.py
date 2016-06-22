# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_auto_20150905_1638'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productorder',
            old_name='order_i',
            new_name='order',
        ),
    ]
