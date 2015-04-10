# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_share', '0006_auto_20150331_0912'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='screenshot',
            field=models.ImageField(null=True, upload_to=b'application_screenshot/'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='applicationcategory',
            name='applications',
            field=models.ManyToManyField(related_name='categories', to='project_share.Application', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='applicationcategory',
            name='description',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='applicationtheme',
            name='description',
            field=models.TextField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
