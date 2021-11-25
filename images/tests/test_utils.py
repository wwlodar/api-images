from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
import base64
from django.test import override_settings
import shutil
from ..utils import path_and_rename

TEST_DIR = 'test_data'

class TestPathAndRename(TestCase):
    def tearDown(self):
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            print(OSError)
    
    @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
    def test_func(self):
        image_data = base64.b64decode("R0lGODlhAQABAIABAP8AAP///yH5BAEAAAEALAAAAAABAAEAAAICRAEAOw==")
        pic = SimpleUploadedFile("file.jpg", image_data, content_type="image/jpg")
        
        print(path_and_rename(instance=pic, filename='something.jpg'))
