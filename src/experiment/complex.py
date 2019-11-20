import json
from timeit import default_timer as timer
import pprint

from api.database import DBConn
from api.models import Models
from api.queries import QueryBuilder


if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    DBConn()
    models = Models()
    model = models.er1['Task']

    with open('obj.json', 'r') as f:
        obj = json.load(f)

    with DBConn.get_session() as session:
        builder = QueryBuilder(session)

        criterion = {
            'field_name': 'Task.name',
            'operator': '==',
            'field_value': obj['name']
        }
        start = timer()
        rec_obj = builder.fetch_one(model, filter_by=[criterion])
        end = timer()
        pp.pprint(rec_obj)
        time = (end - start) * 1000
        print(f"Execution time: {time:.0f} ms")
