# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_userdevice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdevice',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserDevice',
        ),
    ]
