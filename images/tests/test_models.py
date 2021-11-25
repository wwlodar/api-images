from django.test import TestCase
from ..models import AccountTiers,  Link, UserPlan, Image
from django.contrib.auth.models import User
from freezegun import freeze_time
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
import base64
from django.test import override_settings
import shutil

TEST_DIR = 'test_data'


class AccountTiersTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        AccountTiers.objects.create(name='Basic', allowed_sizes=[['200'], ['400']],
                                    choose_exp_time=True, get_link_to_org=True)
    
    def test_name(self):
        account_tier = AccountTiers.objects.get(id=1)
        field_label = account_tier._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')
    
    def test_allowed_sizes(self):
        account_tier = AccountTiers.objects.get(id=1)
        field_label = account_tier._meta.get_field('allowed_sizes').verbose_name
        self.assertEqual(field_label, 'allowed sizes')
    
    def test_choose_exp_time(self):
        account_tier = AccountTiers.objects.get(id=1)
        self.assertEqual(account_tier.choose_exp_time, True)
    
    def test_get_link_to_org(self):
        account_tier = AccountTiers.objects.get(id=1)
        self.assertEqual(account_tier.get_link_to_org, True)


class UserPlanTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        acc = AccountTiers.objects.create(name='Basic', allowed_sizes=[['200'], ['400']],
                                          choose_exp_time=True, get_link_to_org=True)
        
        user = User.objects.create(username='admin', password='password')
        UserPlan.objects.create(user=user, account_tier=acc, pk=1)
    
    def test_user(self):
        user_plan = UserPlan.objects.get(id=1)
        field_label = user_plan._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')
    
    def test_account_tier(self):
        user_plan = UserPlan.objects.get(id=1)
        field_label = user_plan._meta.get_field('account_tier').verbose_name
        self.assertEqual(field_label, 'account tier')


class LinkTest(TestCase):
    @classmethod
    @freeze_time("2021-01-14 03:21:34")
    def setUpTestData(cls):
        acc = AccountTiers.objects.create(name='Basic', allowed_sizes=[['200'], ['400']],
                                          choose_exp_time=True, get_link_to_org=True)
        
        user = User.objects.create(username='admin', password='password')
        user_plan = UserPlan.objects.create(user=user, account_tier=acc)
        link = Link.objects.create(link_to_image='random_link.jpg', expiring_time=300, user=user_plan)
    
    def test_link_to_image(self):
        link = Link.objects.get(id=1)
        field_label = link._meta.get_field('link_to_image').verbose_name
        self.assertEqual(field_label, 'link to image')
    
    def test_link_gen(self):
        link = Link.objects.get(id=1)
        field_label = link._meta.get_field('link_gen').verbose_name
        self.assertEqual(field_label, 'link gen')
    
    def test_exiring_time(self):
        link = Link.objects.get(id=1)
        field_label = link._meta.get_field('expiring_time').verbose_name
        self.assertEqual(field_label, 'expiring time')
        self.assertEqual(link.expiring_time, 300)
    
    def test_expired_date_save_method(self):
        link = Link.objects.get(id=1)
        field_label = link._meta.get_field('expired_date').verbose_name
        self.assertEqual(field_label, 'expired date')
        self.assertEqual(link.expired_date, timezone.make_aware(timezone.datetime(2021, 1, 14, 3, 26, 34)))
    
    def test_user(self):
        link = Link.objects.get(id=1)
        field_label = link._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')


class ImageTest(TestCase):
    def tearDown(self):
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            print(OSError)
    
    @classmethod
    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def setUpTestData(cls):
        acc = AccountTiers.objects.create(name='Basic', allowed_sizes=[['200'], ['400']],
                                          choose_exp_time=True, get_link_to_org=True)
        
        user = User.objects.create(username='admin', password='password')
        user_plan = UserPlan.objects.create(user=user, account_tier=acc)
        image_data = base64.b64decode("R0lGODlhAQABAIABAP8AAP///yH5BAEAAAEALAAAAAABAAEAAAICRAEAOw==")
        pic = SimpleUploadedFile("file.jpg", image_data, content_type="image/jpg")
        Image.objects.create(picture=pic, user=user_plan)
    
    def test_picture(self):
        image = Image.objects.get(id=1)
        field_label = image._meta.get_field('picture').verbose_name
        self.assertEqual(field_label, 'picture')
    
    def test_height(self):
        image = Image.objects.get(id=1)
        field_label = image._meta.get_field('height').verbose_name
        self.assertEqual(field_label, 'height')
        self.assertEqual(image.height, 1)
    
    def test_width(self):
        image = Image.objects.get(id=1)
        field_label = image._meta.get_field('width').verbose_name
        self.assertEqual(field_label, 'width')
        self.assertEqual(image.width, 1)
    
    def test_expiring_time(self):
        image = Image.objects.get(id=1)
        field_label = image._meta.get_field('expiring_time').verbose_name
        self.assertEqual(field_label, 'expiring time')
        self.assertEqual(image.expiring_time, None)
    
    def test_user(self):
        image = Image.objects.get(pk=1)
        field_label = image._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')
