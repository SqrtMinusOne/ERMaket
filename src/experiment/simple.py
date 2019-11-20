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

    with DBConn.get_session() as session:
        builder = QueryBuilder(session)

        criterion = {
            'field_name': 'Task.finish_date',
            'operator': '>',
            'field_value': '2000-01-01'
        }
        order_by = ['Task.finish_date']

        start = timer()
        data = builder.fetch_data(model, filter_by=[criterion],
                                  order_by=order_by, per_page=100000, page=0)
        end = timer()
        # pp.pprint(data)
        print("Length:", len(data))
        time = (end - start) * 1000
        print(f"Execution time: {time:.0f} ms")
