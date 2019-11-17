import stringcase

__all__ = ['NamesConverter']


class NamesConverter:
    @staticmethod
    def db_table_to_class(table_name):
        """DB table name (schema.table_name) to class name

        :param table_name:
        """
        return stringcase.pascalcase(table_name.split('.')[1])
