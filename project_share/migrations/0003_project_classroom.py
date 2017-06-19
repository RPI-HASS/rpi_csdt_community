# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_share', '0002_auto_20141219_0221'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='classroom',
            field=models.ForeignKey(related_name='+', blank=True, to='project_share.Classroom', null=True),
            preserve_default=True,
        ),
    ]
