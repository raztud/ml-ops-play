import hashlib
import io
from pathlib import Path

import boto3

from framework.storage.exceptions import S3StorageNoBucketException
from framework.storage.storage_object_interface import StorageObjectInterface


class S3Storage(StorageObjectInterface):
    def __init__(self, bucket, profile_name=None):
        self.client = boto3.Session(profile_name=profile_name).client("s3")
        self.bucket_name = bucket
        if self.bucket_name is None:
            raise S3StorageNoBucketException("No bucket provided")

    def save(self, file_path, s3_path):
        self.client.upload_file(file_path, self.bucket_name, s3_path)

    def save_buffer(self, file_object: io.BufferedIOBase, s3_path: str):
        """
        :param file_object: io.BufferedIOBase
        :param s3_path: str
        :return:
        """
        self.client.upload_fileobj(file_object, self.bucket_name, s3_path)

    def retrieve(self, s3_path: str) -> io.BufferedIOBase:
        """
        Downloads locally into the specified local_path the file from
        the specified s3_path
        :param s3_path: The file path in S3
        :return: the file descriptor
        """

        fh = io.BytesIO()

        self.client.download_fileobj(self.bucket_name, s3_path, fh)
        fh.seek(0)

        return fh

    def download(self, s3_path, local_path, check_exist=False):
        if check_exist:
            path = Path(local_path)
            if path.is_file():
                local_md5 = hashlib.md5(open(local_path, "rb").read()).hexdigest()
                s3_md5 = self.client.head_object(Bucket=self.bucket_name, Key=s3_path)[
                    "ETag"
                ][1:-1]
                if local_md5 == s3_md5:
                    return True

        fh = self.retrieve(s3_path)
        with open(local_path, "wb") as f:
            f.write(fh.read())

        fh.close()
