from locust import HttpLocust, TaskSet, task, between
import json

FIELD_NAME = None


class Tasks(TaskSet):
    @task(1)
    def entry(self):
        self.client.get(
            url=
            '/entry/er1/Task?filter_by=[{"field_name": "Task.name", "operator": "==", "field_value": "'
            + FIELD_NAME + '"}]'
        )

    @task(2)
    def table(self):
        self.client.get(
            url=
            '/table/er1/Task?order_by=["Task.finish_date"]&filter_by=[{"field_name": "Task.finish_date", "operator": ">", "field_value": "2000-01-01"}]&page=1&per_page=10'
        )


class User(HttpLocust):
    task_set = Tasks
    host = 'http://localhost'
    wait_time = between(5, 9)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        global FIELD_NAME
        if FIELD_NAME is None:
            with open('./experiment/_obj.json', 'r') as f:
                FIELD_NAME = json.load(f)['name']
