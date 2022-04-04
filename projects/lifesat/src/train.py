import argparse
import os

from predictor.livesat_trainer import LivesatTrainer

from framework.model.saving_configuration import SavingConfiguration
from framework.storage.s3_storage import S3Storage

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Training")
    parser.add_argument("--version", help="version", type=str, required=True)
    args = parser.parse_args()

    PROJECT_NAME = os.environ.get("PROJECT")

    predictor = LivesatTrainer()
    model = predictor.train()

    version = args.version

    configuration = SavingConfiguration(
        saver_object=S3Storage(
            bucket=os.environ.get("S3_BUCKET"),
            profile_name=os.environ.get("AWS_PROFILE"),
        ),
        path=f"{PROJECT_NAME}/model-{version}.joblib",
    )

    predictor.save_buffer(
        model=predictor.get_as_bytes(model),
        config=configuration
    )
    print("Done!")

    # for saving just locally
    # from framework.storage.local_storage import LocalStorage
    # configuration = SavingConfiguration(
    #     saver_object=LocalStorage(),
    #     path=f"model-{version}.joblib"
    # )
    #
    # predictor.save_buffer(
    #     model=predictor.get_as_bytes(model),
    #     config=configuration
    # )
