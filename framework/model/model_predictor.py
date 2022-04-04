import os

from framework.model.model_interface import ModelInterface
from framework.storage.s3_storage import S3Storage


class ModelPredictor:
    def __init__(self, project_name, version):
        self._model = None
        self.project_name = project_name
        self.version = version

    def set_model(self, model: ModelInterface):
        self._model = model
        return self

    def predict(self, x_new):
        result = self._model.predict([[x_new]])
        return result[0][0]

    def download_model(self, s3_path, local_path):
        s3 = S3Storage(bucket=os.environ.get("S3_BUCKET"))
        s3.download(
            s3_path=s3_path,
            local_path=local_path,
            check_exist=True,
        )
