# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_delete_advert'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productorder',
            old_name='order',
            new_name='order_i',
        ),
    ]
