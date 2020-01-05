import stringcase

__all__ = ['NamesConverter']


class NamesConverter:
    @staticmethod
    def db_table_to_class(table_name):
        """DB table name (schema.table_name) to class name

        :param table_name:
        """
        return stringcase.pascalcase(table_name.split('.')[1])

    @staticmethod
    def class_name(schema, entity_name):
        return stringcase.pascalcase(schema + '_' + entity_name)

    @staticmethod
    def table_name(entity_name):
        return stringcase.snakecase(stringcase.camelcase(entity_name))

    @staticmethod
    def attribute_name(name):
        return stringcase.snakecase(stringcase.camelcase(name))
