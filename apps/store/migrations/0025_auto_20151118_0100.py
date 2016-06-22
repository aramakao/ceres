# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_mailbox_reply'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedbackseller',
            name='order',
        ),
        migrations.DeleteModel(
            name='Mailbox',
        ),
        migrations.DeleteModel(
            name='FeedbackSeller',
        ),
    ]
