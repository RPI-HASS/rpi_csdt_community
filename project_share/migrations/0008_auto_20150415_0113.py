# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_share', '0007_auto_20150408_0914'),
        ('django_teams', '__first__')
    ]

    operations = [
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
        migrations.AlterField(
            model_name='project',
            name='classroom',
            field=models.ForeignKey(related_name='+', blank=True, to='django_teams.Team', null=True),
            preserve_default=True,
        ),
    ]
