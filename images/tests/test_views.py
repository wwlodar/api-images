from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from ..models import AccountTiers
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import base64
from unittest.mock import patch, mock_open
from django.test import override_settings
import shutil
from ..views import *

TEST_DIR = 'test_data'


class AddImageViewTestCase(APITestCase):
    
    def tearDown(self):
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            print(OSError)
    
    def test_no_auth_provided(self):
        resp = self.client.get('/api/')
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.content, b'{"detail":"Authentication credentials were not provided."}')
    
    def test_incorrect_auth(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + '0f7a6d428f59cea39c5cefb9c271435890b80fee')
        resp = client.get('/api/')
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.content, b'{"detail":"Invalid token."}')
    
    def test_correct_auth_get(self):
        user = User.objects.create_user(username='admin')
        token = Token.objects.get(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        resp = client.get('/api/')
        self.assertEqual(resp.status_code, 405)
        self.assertEqual(resp.content, b'{"detail":"Method \\"GET\\" not allowed."}')
    
    def test_correct_auth_post_incorrect_file(self):
        acc = AccountTiers.objects.create(name='Basic', allowed_sizes=[200, 400], choose_exp_time=False,
                                          get_link_to_org=False)
        user = User.objects.create_user(username='admin')
        user_with_plan = UserPlan.objects.create(user=user, account_tier=acc)
        token = Token.objects.get(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        pic = SimpleUploadedFile("file.jpg", b"file_content", content_type="image/jpg")
        resp = client.post('/api/', {'picture': pic})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content,
                         b'{"picture":["Upload a valid image. The file you uploaded was either not an image or a corrupted image."]}'
                         )
    
    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_correct_auth_post_correct_file(self):
        acc = AccountTiers.objects.create(name='Basic', allowed_sizes=[200, 400], choose_exp_time=False,
                                          get_link_to_org=False)
        user = User.objects.create_user(username='admin')
        user_with_plan = UserPlan.objects.create(user=user, account_tier=acc)
        token = Token.objects.get(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        image_data = base64.b64decode("R0lGODlhAQABAIABAP8AAP///yH5BAEAAAEALAAAAAABAAEAAAICRAEAOw==")
        pic = SimpleUploadedFile("file.jpg", image_data, content_type="image/jpg")
        resp = client.post('/api/', {'picture': pic})
        
        self.assertEqual(resp.status_code, 200)
        self.assertIn('links', str(resp.content))
        self.assertIn(str(acc.allowed_sizes[0]), str(resp.content))
        self.assertIn(str(acc.allowed_sizes[1]), str(resp.content))
    
    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_correct_auth_post_correct_file_with_expired_link(self):
        acc = AccountTiers.objects.create(name='Basic', allowed_sizes=[200, 400], choose_exp_time=True,
                                          get_link_to_org=False)
        user = User.objects.create_user(username='admin')
        user_with_plan = UserPlan.objects.create(user=user, account_tier=acc)
        token = Token.objects.get(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        image_data = base64.b64decode("R0lGODlhAQABAIABAP8AAP///yH5BAEAAAEALAAAAAABAAEAAAICRAEAOw==")
        pic = SimpleUploadedFile("file.jpg", image_data, content_type="image/jpg")
        resp = client.post('/api/', {'picture': pic, 'choose_exp_time': 300})
        
        self.assertEqual(resp.status_code, 200)
        self.assertIn('links', str(resp.content))
        self.assertIn(str(acc.allowed_sizes[0]), str(resp.content))
        self.assertIn(str(acc.allowed_sizes[1]), str(resp.content))


class ImagesListViewTestCase(APITestCase):
    def tearDown(self):
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            print(OSError)
    
    def test_no_auth_provided(self):
        resp = self.client.get('/api/list/')
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.content, b'{"detail":"Authentication credentials were not provided."}')
    
    def test_incorrect_auth(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + '0f7a6d428f59cea39c5cefb9c271435890b80fee')
        resp = client.get('/api/list/')
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.content, b'{"detail":"Invalid token."}')
    
    def test_correct_auth_empty_list(self):
        acc = AccountTiers.objects.create(name='Basic', allowed_sizes=[200, 400], choose_exp_time=False,
                                          get_link_to_org=False)
        user = User.objects.create_user(username='admin')
        user_with_plan = UserPlan.objects.create(user=user, account_tier=acc)
        token = Token.objects.get(user=user)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        resp = client.get('/api/list/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content, b'[]')
    
    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_correct_auth_two_users(self):
        image_data = base64.b64decode("R0lGODlhAQABAIABAP8AAP///yH5BAEAAAEALAAAAAABAAEAAAICRAEAOw==")
        pic = SimpleUploadedFile("file.jpg", image_data, content_type="image/jpg")
        
        acc = AccountTiers.objects.create(name='Basic', allowed_sizes=[200, 400], choose_exp_time=False,
                                          get_link_to_org=False)
        user1 = User.objects.create_user(username='admin1')
        user_with_plan1 = UserPlan.objects.create(user=user1, account_tier=acc)
        token1 = Token.objects.get(user=user1)
        image1 = Image.objects.create(user=user_with_plan1, picture=pic)
        link1 = Link.objects.create(user=user_with_plan1, link_to_image=image1.picture.url)
        
        user2 = User.objects.create_user(username='admin')
        user_with_plan2 = UserPlan.objects.create(user=user2, account_tier=acc)
        token2 = Token.objects.get(user=user2)
        image2 = Image.objects.create(user=user_with_plan2, picture=pic)
        link2 = Link.objects.create(user=user_with_plan2, link_to_image=image2.picture.url)

        
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token2.key)
        resp = client.get('/api/list/')

        self.assertEqual(resp.status_code, 200)
        self.assertNotIn(str(image1.picture), str(resp.content))


class LoginViewTestCase(APITestCase):
    def test_incorrect_login(self):
        user = User.objects.create_user(username='admin', password='password')
        client = APIClient()
        resp = client.post('/api/api-login', {'username': 'admin', 'password': 'incorrect_password'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.content, b'{"non_field_errors":["Unable to log in with provided credentials."]}')
    
    def test_correct_login(self):
        user = User.objects.create_user(username='admin', password='password')
        client = APIClient()
        resp = client.post('/api/api-login', data={'username': 'admin', 'password': 'password'})
        self.assertEqual(resp.status_code, 200)
        self.assertIn(str(Token.objects.get(user=user)), str(resp.content))


class ImageAccessTest(APITestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="data")
    def test_no_time_expiring(self, mock_file):
        acc = AccountTiers.objects.create(name='Basic', allowed_sizes=[200, 400],
                                          choose_exp_time=True, get_link_to_org=True)
        
        user = User.objects.create(username='admin', password='password')
        user_plan = UserPlan.objects.create(user=user, account_tier=acc)
        link = Link.objects.create(link_to_image='/media/image/Gv8eN3ofiegUJTZgCAkWaZ.jpg', user=user_plan)
        
        client = APIClient()
        resp = client.get('/api/' + link.link_gen)
        self.assertEqual(resp.status_code, 200)
    
    @patch("builtins.open", new_callable=mock_open, read_data="data")
    def test_date_not_expired(self, mock_file):
        acc = AccountTiers.objects.create(name='Basic', allowed_sizes=[200, 400],
                                          choose_exp_time=True, get_link_to_org=True)
        
        user = User.objects.create(username='admin', password='password')
        user_plan = UserPlan.objects.create(user=user, account_tier=acc)
        link = Link.objects.create(link_to_image='/media/image/Gv8eN3ofiegUJTZgCAkWaZ.jpg', expiring_time=300,
                                   expired_date=("2021-01-14 03:21:34"),
                                   user=user_plan)
        
        client = APIClient()
        resp = client.get('/api/' + link.link_gen)
        self.assertEqual(resp.status_code, 200)
    
    def test_date_expired(self):
        acc = AccountTiers.objects.create(name='Basic', allowed_sizes=[200, 400],
                                          choose_exp_time=True, get_link_to_org=True)
        
        user = User.objects.create(username='admin', password='password')
        user_plan = UserPlan.objects.create(user=user, account_tier=acc)
        link = Link.objects.create(link_to_image='/media/image/Gv8eN3ofiegUJTZgCAkWaZ.jpg',
                                   expired_date="2021-01-10 03:29:34",
                                   user=user_plan)
        
        client = APIClient()
        resp = client.get('/api/' + link.link_gen)
        self.assertEqual(resp.status_code, 403)
        self.assertEqual(resp.content, b'Access to this link has expired.')
