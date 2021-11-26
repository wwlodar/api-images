from rest_framework import serializers
from django.contrib.auth.models import User
from django.test import TestCase
from ..models import Image, AccountTiers, UserPlan
from ..serializers import TokenSerializer, LoginSerializers, ImageSerializer, ImageExpiredLinkSerializer
from django.core.files.uploadedfile import SimpleUploadedFile
import base64
from django.test import override_settings
import shutil
from rest_framework.authtoken.models import Token
from django.test import RequestFactory

TEST_DIR = 'test_data'
import mock


class TestImageSerializer(TestCase):
    def tearDown(self):
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            print(OSError)
    
    @classmethod
    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def setUp(self):
        image_data = base64.b64decode("R0lGODlhAQABAIABAP8AAP///yH5BAEAAAEALAAAAAABAAEAAAICRAEAOw==")
        pic = SimpleUploadedFile("file.jpg", image_data, content_type="image/jpg")
        acc = AccountTiers.objects.create(name='Basic', allowed_sizes=[['200'], ['400']],
                                          choose_exp_time=True, get_link_to_org=True)
        
        user = User.objects.create(username='admin', password='password')
        user_plan = UserPlan.objects.create(user=user, account_tier=acc)
        
        data = {'picture': pic, 'user': user_plan}
        
        self.img_attributes = data
        
        self.img = Image.objects.create(**self.img_attributes)
        self.serializer = ImageSerializer(instance=self.img)
    
    def test_contains_expected_fields(self):
        data = self.serializer.data
        
        self.assertCountEqual(data.keys(), ['picture'])
    
    def test_field_content(self):
        data = self.serializer.data
        
        self.assertFalse(None, data['picture'])


class TestImageExpiredLinkSerializer(TestCase):
    def tearDown(self):
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            print(OSError)
    
    @classmethod
    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def setUp(self):
        image_data = base64.b64decode("R0lGODlhAQABAIABAP8AAP///yH5BAEAAAEALAAAAAABAAEAAAICRAEAOw==")
        pic = SimpleUploadedFile("file.jpg", image_data, content_type="image/jpg")
        acc = AccountTiers.objects.create(name='Basic', allowed_sizes=[['200'], ['400']],
                                          choose_exp_time=True, get_link_to_org=True)
        
        user = User.objects.create_user(username='admin', password='password')
        user_plan = UserPlan.objects.create(user=user, account_tier=acc)
        
        data = {'picture': pic, 'user': user_plan, 'expiring_time': 300}
        
        self.img_attributes = data
        
        self.img = Image.objects.create(**self.img_attributes)
        self.serializer = ImageExpiredLinkSerializer(instance=self.img)
    
    def test_contains_expected_fields(self):
        data = self.serializer.data
        
        self.assertCountEqual(data.keys(), ['picture', 'expiring_time'])
    
    def test_field_content(self):
        data = self.serializer.data
        
        self.assertFalse(None, data['picture'])
        self.assertEqual(data['expiring_time'], 300)


class TestLoginSerializer(TestCase):
    @mock.patch("images.serializers.authenticate", autospec=True)
    def test_valid_data(self, mock_auth):
        user = User.objects.create(username='admin', password='password')
        request1 = RequestFactory().post('/api/api-login/')
        data = {'username': user.username, 'password': 'invalid'}
        serializer = LoginSerializers(data=data, context={'request': request1})
        
        self.assertEqual(serializer.is_valid(), True)
        self.assertEqual(serializer.data['username'], user.username)
    
    @mock.patch("images.serializers.authenticate", autospec=True)
    def test_invalid_data(self, mock_auth):
        user = User.objects.create(username='admin', password='password')
        request1 = RequestFactory().post('/api/api-login/')
        mock_auth.return_value = None
        data = {'username': user.username, 'password': 'invalid'}
        serializer = LoginSerializers(data=data, context={'request': request1})
        
        self.assertEqual(serializer.is_valid(), False)

    def test_missing_data(self):
        user = User.objects.create(username='admin', password='password')
        request1 = RequestFactory().post('/api/api-login/')

        data = {'username': user.username}
        serializer = LoginSerializers(data=data, context={'request': request1})
    
        self.assertEqual(serializer.is_valid(), False)

class TestTokenSerializer(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='admin', password='password')
        self.token = Token.objects.create(user=user)
        
        self.serializer = TokenSerializer(instance = self.token)
        

    def test_contains_expected_fields(self):
        data = self.serializer.data
    
        self.assertCountEqual(data.keys(), ['key'])

    def test_field_content(self):
        data = self.serializer.data
    
        self.assertEquals(data['key'], self.token.key)
