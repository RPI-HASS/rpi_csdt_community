# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-24 17:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import project_share.models


class Migration(migrations.Migration):

    dependencies = [
        ('project_share', '0020_application_rank'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='extendeduser',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='extendeduser',
            name='avatar',
            field=project_share.models.FileField(blank=True, null=True, upload_to=project_share.models.my_awesome_upload_function),
        ),
        migrations.AddField(
            model_name='extendeduser',
            name='bio',
            field=models.CharField(blank=True, default=b'', max_length=240),
        ),
        migrations.AddField(
            model_name='extendeduser',
            name='display_name',
            field=models.CharField(default=b'', max_length=70),
        ),
        migrations.AlterField(
            model_name='extendeduser',
            name='date_joined',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='extendeduser',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='extendeduser',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='extendeduser',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='extendeduser',
            name='username',
            field=models.CharField(max_length=40, unique=True),
        ),
    ]
