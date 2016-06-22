# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_productorder_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedbackbuyer',
            name='order',
        ),
        migrations.DeleteModel(
            name='FeedbackBuyer',
        ),
    ]
