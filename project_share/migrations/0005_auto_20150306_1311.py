# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_share', '0004_application_featured'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Library',
        ),
        migrations.RemoveField(
            model_name='application',
            name='module',
        ),
        migrations.DeleteModel(
            name='Module',
        ),
    ]
