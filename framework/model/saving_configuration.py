from dataclasses import dataclass

from framework.storage.storage_object_interface import StorageObjectInterface


@dataclass
class SavingConfiguration:
    saver_object: StorageObjectInterface
    aws_profile: str = None
    path: str = None
