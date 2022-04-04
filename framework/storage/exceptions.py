class S3StorageException(Exception):
    pass


class S3StorageNoBucketException(S3StorageException):
    pass
