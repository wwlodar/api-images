# Generated by Django 3.2.9 on 2021-11-23 14:21

from django.db import migrations, models
import easy_thumbnails.fields
import images.utils


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0010_alter_image_expiring_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounttiers',
            name='name',
            field=models.CharField(default=1, max_length=120),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='image',
            name='picture',
            field=easy_thumbnails.fields.ThumbnailerImageField(blank=True, upload_to=images.utils.path_and_rename),
        ),
    ]