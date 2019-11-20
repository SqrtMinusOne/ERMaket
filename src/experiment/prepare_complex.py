import json
import pprint

import sqlalchemy as sa

from api.database import DBConn
from api.models import Models

COMPLEX_QUERY = lambda task_name: f"""SELECT * FROM er1.task
LEFT JOIN er1.user_on_task ON task.name = user_on_task.task_name
LEFT JOIN er1.attachment ON task.name = attachment.task_name
LEFT JOIN er1.subtask ON task.name = subtask.task_name
WHERE er1.task.name = '{task_name}';
"""

if __name__ == "__main__":
    pp = pprint.PrettyPrinter(indent=4)

    DBConn()
    models = Models()

    with DBConn.get_session() as session:
        q = session.query(models.er1['Task']) \
            .order_by(sa.func.random()).first()
        obj = q.__marshmallow__().dump(q)

         # pp.pprint(obj)
        with open('obj.json', 'w') as f:
            json.dump(obj, f)

    with open('./experiment/sql_queries/complex.sql', 'w') as f:
        f.write(COMPLEX_QUERY(obj['name']))

    with open('./experiment/_obj.json', 'w') as f:
        json.dump(obj, f)
