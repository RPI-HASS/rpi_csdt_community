# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_share', '0003_project_classroom'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='featured',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
