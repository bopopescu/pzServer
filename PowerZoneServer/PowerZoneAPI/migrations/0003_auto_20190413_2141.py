# Generated by Django 2.1.4 on 2019-04-13 19:41

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PowerZoneAPI', '0002_auto_20190320_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locale',
            name='coordinate',
            field=django.contrib.gis.db.models.fields.PointField(geography=True, srid=4326),
        ),
    ]
