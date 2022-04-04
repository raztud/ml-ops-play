import os

from api.models import LivesatPrediction
from predictor.livesat_model import LivesatModel

from framework.api.main import ServingApp, start_app

app = ServingApp(LivesatModel, LivesatPrediction)
start_app(app)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=os.environ.get("PORT", 8080))
