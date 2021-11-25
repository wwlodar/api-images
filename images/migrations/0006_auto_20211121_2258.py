# Generated by Django 3.2.9 on 2021-11-21 21:58

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0005_auto_20211121_2204'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='height',
        ),
        migrations.RemoveField(
            model_name='image',
            name='picture',
        ),
        migrations.RemoveField(
            model_name='link',
            name='image',
        ),
        migrations.AddField(
            model_name='image',
            name='headshot',
            field=versatileimagefield.fields.VersatileImageField(default=1, upload_to='headshots/', verbose_name='Headshot'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='image',
            name='headshot_ppoi',
            field=versatileimagefield.fields.PPOIField(default='0.5x0.5', editable=False, max_length=20),
        ),
    ]