import io
import shutil

from framework.storage.storage_object_interface import StorageObjectInterface


class LocalStorage(StorageObjectInterface):
    def __init__(self):
        pass

    def save(self, file_path, path):
        shutil.copyfile(file_path, path)

    def save_buffer(self, file_object: io.BufferedIOBase, path: str):
        with open(path, "wb") as f:
            f.write(file_object.read())

    def retrieve(self, *args, **kwargs):
        pass
