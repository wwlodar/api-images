# Generated by Django 3.2.9 on 2021-11-25 20:31

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0013_auto_20211124_1736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounttiers',
            name='allowed_sizes',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=10), size=None),
        ),
    ]
