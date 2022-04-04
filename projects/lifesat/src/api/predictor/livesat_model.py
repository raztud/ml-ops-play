import logging

from joblib import load

from api.models import LivesatRequestModel
from framework.model.model_interface import ModelInterface
from framework.model.model_predictor import ModelPredictor

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class LivesatModel:
    def __init__(self, project, version, lazy=False):
        self._project_name = project
        self._version = version
        self.predictor: ModelPredictor = ModelPredictor(
            self._project_name, version=self._version
        )
        self._model = None

        if not lazy:
            self._model = self.load_model()
            self.predictor.set_model(self._model)

    def predict(self, request: LivesatRequestModel):
        x_new = request.gdp
        if not self._model:
            self._model = self.load_model()
            self.predictor.set_model(self._model)

        return self.predictor.predict(x_new)

    def load_model(self) -> ModelInterface:
        logger.debug("Loading model...")

        local_path = f"/tmp/model-{self._project_name}-{self._version}.joblib"
        s3_path = f"{self._project_name}/model-{self._version}.joblib"

        self.predictor.download_model(
            s3_path=s3_path,
            local_path=local_path,
        )

        return load(local_path)
