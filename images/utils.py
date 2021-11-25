import base64
import hashlib
import os
import shortuuid


def namer(thumbnailer, prepared_options, source_filename,
          thumbnail_extension, **kwargs):
    parts = ':'.join([source_filename] + prepared_options)
    short_sha = hashlib.sha1(parts.encode('utf-8')).digest()
    short_hash = base64.urlsafe_b64encode(short_sha[:9]).decode('utf-8')
    return '.'.join([short_hash, thumbnail_extension])


def path_and_rename(instance, filename):
    upload_to = 'image/'
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(shortuuid.uuid(), ext)
    return os.path.join(upload_to, filename)
