from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from easy_thumbnails.fields import ThumbnailerImageField
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime, timedelta
from .utils import path_and_rename
from pathlib import Path


class AccountTiers(models.Model):
    name = models.CharField(max_length=120)
    allowed_sizes = ArrayField(
            models.CharField(max_length=10, blank=True),
    )
    choose_exp_time = models.BooleanField()
    get_link_to_org = models.BooleanField()
    
    class Meta:
        verbose_name_plural = "AccountTiers"
        
    def __str__(self):
        return self.name


class UserPlan(models.Model):
    account_tier = models.ForeignKey(AccountTiers, on_delete=models.CASCADE)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)


class Image(models.Model):
    picture = ThumbnailerImageField(upload_to=path_and_rename, blank=True)
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    user = models.ForeignKey(UserPlan, on_delete=models.CASCADE)
    expiring_time = models.IntegerField(default=None, null=True, validators=[
        MaxValueValidator(30000),
        MinValueValidator(300)
    ])
    
    def save(self, *args, **kwargs):
        self.height = self.picture.height
        self.width = self.picture.width
        super(Image, self).save(*args, **kwargs)


class Link(models.Model):
    link_gen = models.CharField(max_length=200)
    link_to_image = models.CharField(max_length=200)
    expiring_time = models.IntegerField(default=None, null=True)
    expired_date = models.DateTimeField(null=True)
    user = models.ForeignKey(UserPlan, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        if self.expiring_time is not None:
            self.expired_date = datetime.now() + timedelta(seconds=float(self.expiring_time))
        self.link_gen = 'image/' + Path(self.link_to_image).stem
        super(Link, self).save(*args, **kwargs)
        
    def get_absolute(self):
        return self.request(self.link_gen)
