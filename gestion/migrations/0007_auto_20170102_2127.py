# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-02 20:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0006_auto_20170102_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='followed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='who_is_followed', to='gestion.UserProfile'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='who_follows', to='gestion.UserProfile'),
        ),
    ]
