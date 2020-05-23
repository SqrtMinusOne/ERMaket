from collections import deque
from locust import HttpUser, TaskSet, task

import logging
import pandas as pd

from config import Config


CREDENTIALS = None


class LoginTasks(TaskSet):
    def on_start(self):
        if len(CREDENTIALS) > 0:
            self.login, self.password = CREDENTIALS.pop()
        else:
            self.login, self.password = Config.FALLBACK_CREDS
            logging.warning('Not enough credentials for Locust')

    # def on_stop(self):
    #     self.client.post("/auth/logout")

    @task(1)
    def login(self):
        self.client.post("/auth/login", {
            "login": self.login,
            "password": self.password,
        })
        # self.client.post("/auth/logout")


class LoginUser(HttpUser):
    tasks = {LoginTasks: 1}
    min_wait = Config.MIN_WAIT
    max_wait = Config.MAX_WAIT
    host = Config.HOST

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        global CREDENTIALS
        if CREDENTIALS is None:
            df = pd.read_csv(Config.CREDS_CSV)
            CREDENTIALS = deque(df[['login', 'password']].values.tolist())
