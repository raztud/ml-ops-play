import io
import os
import pickle
import urllib.request

import numpy as np
import pandas as pd
import sklearn.linear_model

from framework.model.train_interface import TrainInterface

DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml/master/"
DATAPATH = os.path.join("datasets", "lifesat", "")


class LivesatTrainer(TrainInterface):
    def train(self):
        bli, gdps = self.load_data()
        country_stats = self.__prepare_country_stats(bli, gdps)
        # visualise_data(country_stats)

        X = np.c_[country_stats["GDP per capita"]]
        y = np.c_[country_stats["Life satisfaction"]]

        m = sklearn.linear_model.LinearRegression()
        return self._train(m, X, y)

    def load_data(self):
        self.__download_data()

        oecd_bli = pd.read_csv(DATAPATH + "oecd_bli_2015.csv", thousands=",")
        gdp_per_capita = pd.read_csv(
            DATAPATH + "gdp_per_capita.csv",
            thousands=",",
            delimiter="\t",
            encoding="latin1",
            na_values="n/a",
        )

        return oecd_bli, gdp_per_capita

    @staticmethod
    def get_as_bytes(data: object) -> io.BufferedIOBase:
        fh = io.BytesIO()
        pickle.dump(data, fh, pickle.HIGHEST_PROTOCOL)
        fh.seek(0)

        return fh

    @staticmethod
    def _train(model_instance, X, y):
        # Train the model
        model_instance.fit(X, y)

        return model_instance

    @staticmethod
    def __download_data():
        os.makedirs(DATAPATH, exist_ok=True)
        for filename in ("oecd_bli_2015.csv", "gdp_per_capita.csv"):
            url = "{}/datasets/lifesat/{}".format(DOWNLOAD_ROOT, filename)
            fullpath = DATAPATH + filename
            if not os.path.isfile(fullpath):
                urllib.request.urlretrieve(url, fullpath)

    @staticmethod
    def __prepare_country_stats(oecd_bli, gdp_per_capita):
        oecd_bli = oecd_bli[oecd_bli["INEQUALITY"] == "TOT"]
        oecd_bli = oecd_bli.pivot(index="Country", columns="Indicator", values="Value")
        gdp_per_capita.rename(columns={"2015": "GDP per capita"}, inplace=True)
        gdp_per_capita.set_index("Country", inplace=True)
        full_country_stats = pd.merge(
            left=oecd_bli, right=gdp_per_capita, left_index=True, right_index=True
        )
        full_country_stats.sort_values(by="GDP per capita", inplace=True)
        remove_indices = [0, 1, 6, 8, 33, 34, 35]
        keep_indices = list(set(range(36)) - set(remove_indices))
        return full_country_stats[["GDP per capita", "Life satisfaction"]].iloc[
            keep_indices
        ]
