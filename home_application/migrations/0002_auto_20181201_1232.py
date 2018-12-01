# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitorhostdata',
            name='time',
            field=models.DateTimeField(),
        ),
    ]
