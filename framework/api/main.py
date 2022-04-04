import os
import time
from typing import Union, Type

from pydantic import BaseModel

from framework.logging.ml_logging import logging
from fastapi import FastAPI, Request

from framework.model.model_interface import ModelInterface
from framework.monitoring.logger_metric import LoggerMetric
from framework.monitoring.metric import Metric


class ServingApp(FastAPI):
    def __init__(self, model_class, response_model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_class = model_class
        self.model: Union[ModelInterface, None] = None
        self.metrics = LoggerMetric()
        self.response_model: Type[BaseModel] = response_model


def start_app(app: ServingApp):
    @app.on_event("startup")
    async def startup():
        logging.info(f"Start application with model {app.model_class}")
        app.model = app.model_class(
            project=os.environ.get("PROJECT"), version=os.environ.get("version", 12)
        )

    @app.get("/ping")
    async def ping():
        return {"hello": os.environ.get("PROJECT", "world")}

    @app.post("/predict", response_model=app.response_model)
    async def predict(request: BaseModel):
        return {
            "prediction": app.model.predict(request),
        }

    @app.middleware("http")
    async def process_time_metric(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logging.info(f"Path: {request.scope['path']}")

        slug_path = request.scope["path"].replace("/", "_").lstrip("_")
        tags = Metric.get_default_tags()

        app.metrics.add_metric(
            f"process_{slug_path}",
            process_time,
            tags=tags,
        )

        app.metrics.add_count(
            f"process_{slug_path}",
            tags=tags,
        )

        return response
