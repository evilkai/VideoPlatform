from storages.backends.s3boto3 import S3Boto3Storage
import boto3
from botocore.client import Config

class MediaStorage(S3Boto3Storage):
    bucket_name = 'public-data-bucket'
    custom_domain = 's3.storage.selcloud.ru'
    file_overwrite = False

    def __init__(self, *args, **kwargs):
        kwargs['custom_domain'] = self.custom_domain
        kwargs['bucket_name'] = self.bucket_name
        kwargs['file_overwrite'] = self.file_overwrite
        super().__init__(*args, **kwargs)

    def _get_s3_client(self):
        session = boto3.session.Session()
        return session.client(
            's3',
            aws_access_key_id='24e4f1089a024ef081cb51b49a1d8c7c',
            aws_secret_access_key='e6cb6a1da98d4a3595c2bc9f26907e5d',
            endpoint_url='https://s3.storage.selcloud.ru',
            config=Config(signature_version='s3v4', retries={'max_attempts': 10, 'mode': 'standard'}),
            verify=False  # Отключение проверки SSL
        )
