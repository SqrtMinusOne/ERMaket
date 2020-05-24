import logging
import json
from collections import deque

import numpy as np
import pandas as pd
from locust import HttpUser, TaskSet, task

from config import Config

CREDENTIALS = None
FIELD_NAME = 'Janet Wyatt'


class ReadTasks(TaskSet):
    def on_start(self):
        if len(CREDENTIALS) > 0:
            self.login, self.password = CREDENTIALS.pop()
            # self.login, self.password = CREDENTIALS[0]
        else:
            self.login, self.password = Config.FALLBACK_CREDS
            logging.warning('Not enough credentials for Locust')

        self.client.post(
            "/auth/login", {
                "login": self.login,
                "password": self.password,
            }
        )

    def on_stop(self):
        self.client.post('/auth/logout')

    @task(3)
    def entry(self):
        self.client.get(
            url='/tables/entry/er1/task?filter_by=[{"field_name": "name", "operator": "==", "field_value": "'
            + FIELD_NAME + '"}]'
        )

    @task(5)
    def table_filter(self):
        self.client.get(
            url='/tables/table/er1/task?filter_by={"and":[{"field_name":"name","operator":"icontains","field_value":"cra"}],"or":[]}&offset=0&limit=100'
        )

    @task(10)
    def table_all(self):
        self.client.get(url='/tables/table/er1/task?offset=0&limit=100')

    @task(8)
    def table_last(self):
        self.client.get(url='/tables/table/er1/task?offset=100000&limit=100')

    @task(1)
    def add_task(self):
        transaction = {
            Config.ENTRY_ID: {
                'create': {
                    'dummy_key': {
                        'newData': {
                            "name": "dummy",
                            "due_date": "2020-05-23T19:12:06.981Z",
                            "description": "dummy",
                            "list_id": np.random.randint(1, 30)
                        },
                        'links': []
                    }
                }
            }
        }
        self.client.post(
            url='/transaction/execute',
            data=json.dumps({'transaction': transaction}),
            headers={
                'Content-Type': 'application/json'
            }
        )


class ReadUser(HttpUser):
    tasks = {ReadTasks: 1}
    min_wait = Config.MIN_WAIT
    max_wait = Config.MAX_WAIT
    host = Config.HOST

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        global CREDENTIALS
        if CREDENTIALS is None:
            df = pd.read_csv(Config.CREDS_CSV)
            CREDENTIALS = deque(df[['login', 'password']].values.tolist())
